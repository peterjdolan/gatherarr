"""Scheduler for periodic search operations."""

import asyncio
import time
from typing import Any, Protocol

import structlog

from app.arr_client import ArrClient
from app.config import ArrTarget
from app.metrics import (
  grabs_total,
  last_success_timestamp_seconds,
  request_duration_seconds,
  request_errors_total,
  requests_total,
  run_total,
  skips_total,
  state_write_failures_total,
)
from app.state import ItemState, RunStatus, StateManager, TargetState

logger = structlog.get_logger()


class ItemHandler(Protocol):
  """Protocol for handling individual items."""

  def extract_id(self, item: dict[str, Any]) -> tuple[int | None, str]:
    """Extract item ID and identifier for logging."""
    ...

  async def search(self, client: ArrClient, item_id: int) -> None:
    """Trigger search for the item."""
    ...

  def log_error(self, target_name: str, item_identifier: str, error: Exception) -> None:
    """Log error for the item."""
    ...


class Scheduler:
  """Schedules and executes periodic search operations."""

  def __init__(
    self,
    config_targets: list[ArrTarget],
    state_manager: StateManager,
    arr_clients: dict[str, ArrClient],
  ) -> None:
    self.config_targets = config_targets
    self.state_manager = state_manager
    self.arr_clients = arr_clients
    self.running = False

  async def run_once(self, target: ArrTarget) -> None:
    """Execute a single run for a target."""
    target_state = self.state_manager.get_target_state(target.name)
    now = time.time()

    target_state.last_run_timestamp = now
    run_id = f"{target.name}-{int(now)}"

    logger.info(
      "Starting run",
      target=target.name,
      type=target.arr_type.value,
      run_id=run_id,
    )
    logger.debug(
      "Run configuration",
      target=target.name,
      type=target.arr_type.value,
      run_id=run_id,
      ops_per_interval=target.ops_per_interval,
      interval_s=target.interval_s,
      item_revisit_timeout_s=target.item_revisit_timeout_s,
    )

    try:
      client = self.arr_clients[target.name]
      start_time = time.time()

      logger.debug(
        "Fetching items",
        target=target.name,
        type=target.arr_type.value,
        run_id=run_id,
      )
      if target.arr_type.value == "radarr":
        items = await client.get_movies()
        handler: ItemHandler = MovieHandler()
      else:
        items = await client.get_series()
        handler = SeriesHandler()
      logger.debug(
        "Items fetched",
        target=target.name,
        type=target.arr_type.value,
        run_id=run_id,
        item_count=len(items),
      )

      processed = await self._process_items(
        target, client, items, target_state, now, run_id, handler
      )

      duration_ms = int((time.time() - start_time) * 1000)
      target_state.last_success_timestamp = now
      target_state.last_status = RunStatus.SUCCESS
      target_state.consecutive_failures = 0
      target_state.last_error_summary = ""

      last_success_timestamp_seconds.labels(target=target.name, type=target.arr_type.value).set(now)
      run_total.labels(target=target.name, type=target.arr_type.value, status="success").inc()

      logger.info(
        "Run completed",
        target=target.name,
        type=target.arr_type.value,
        run_id=run_id,
        status="success",
        duration_ms=duration_ms,
        processed=processed,
      )
    except Exception as e:
      error_msg = str(e)[:200]
      target_state.last_status = RunStatus.ERROR
      target_state.consecutive_failures += 1
      target_state.last_error_summary = error_msg

      run_total.labels(target=target.name, type=target.arr_type.value, status="error").inc()
      request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()

      logger.error(
        "Run failed",
        target=target.name,
        type=target.arr_type.value,
        run_id=run_id,
        status="error",
        error=error_msg,
        consecutive_failures=target_state.consecutive_failures,
      )

      # Warn if consecutive failures are accumulating
      if target_state.consecutive_failures >= 3:
        logger.warning(
          "Multiple consecutive run failures",
          target=target.name,
          type=target.arr_type.value,
          consecutive_failures=target_state.consecutive_failures,
          last_error=error_msg,
        )

    self.state_manager.state.total_runs += 1
    try:
      self.state_manager.save()
    except Exception as e:
      logger.error("Failed to save state", error=str(e))
      state_write_failures_total.inc()

  async def start(self) -> None:
    """Start the scheduler loop."""
    self.running = True
    logger.info("Scheduler started", targets=len(self.config_targets))

    while self.running:
      tasks = []
      for target in self.config_targets:
        target_state = self.state_manager.get_target_state(target.name)
        now = time.time()
        time_since_last = now - target_state.last_run_timestamp

        if time_since_last >= target.interval_s:
          tasks.append(self.run_once(target))

      if tasks:
        logger.debug("Executing scheduled tasks", task_count=len(tasks))
        await asyncio.gather(*tasks, return_exceptions=True)
      else:
        logger.debug("No tasks to execute, sleeping")

      await asyncio.sleep(10)

  def stop(self) -> None:
    """Stop the scheduler."""
    self.running = False
    logger.info("Scheduler stopped")

  async def _process_items(
    self,
    target: ArrTarget,
    client: ArrClient,
    items: list[dict[str, Any]],
    target_state: TargetState,
    now: float,
    run_id: str,
    item_handler: ItemHandler,
  ) -> int:
    """Process items and trigger searches using the provided handler."""
    processed = 0
    ops_count = 0

    logger.debug(
      "Processing items",
      target=target.name,
      type=target.arr_type.value,
      run_id=run_id,
      total_items=len(items),
      ops_per_interval=target.ops_per_interval,
    )

    for item in items:
      if ops_count >= target.ops_per_interval:
        logger.debug(
          "Reached ops_per_interval limit",
          target=target.name,
          type=target.arr_type.value,
          run_id=run_id,
          ops_count=ops_count,
          ops_per_interval=target.ops_per_interval,
        )
        break

      item_id, item_identifier = item_handler.extract_id(item)
      if item_id is None:
        logger.warning(
          "Skipping item with no ID",
          target=target.name,
          type=target.arr_type.value,
          run_id=run_id,
          item_identifier=item_identifier,
        )
        continue

      item_id_str = str(item_id)
      item_state = target_state.items.get(item_id_str)

      if item_state is not None:
        time_since_last = now - item_state.last_processed_timestamp
        if time_since_last < target.item_revisit_timeout_s:
          logger.debug(
            "Skipping item (revisit timeout not met)",
            target=target.name,
            type=target.arr_type.value,
            run_id=run_id,
            item_id=item_id_str,
            item_identifier=item_identifier,
            time_since_last=time_since_last,
            revisit_timeout=target.item_revisit_timeout_s,
          )
          skips_total.labels(target=target.name, type=target.arr_type.value).inc()
          continue

      try:
        logger.info(
          "Triggering search for item",
          target=target.name,
          type=target.arr_type.value,
          run_id=run_id,
          item_id=item_id_str,
          item_identifier=item_identifier,
        )
        request_start = time.time()
        requests_total.labels(target=target.name, type=target.arr_type.value).inc()
        await item_handler.search(client, item_id)
        request_duration = time.time() - request_start
        request_duration_seconds.labels(target=target.name, type=target.arr_type.value).observe(
          request_duration
        )

        target_state.items[item_id_str] = ItemState(
          item_id=item_id_str,
          last_processed_timestamp=now,
          last_result="search_triggered",
          last_status="success",
        )

        grabs_total.labels(target=target.name, type=target.arr_type.value).inc()
        processed += 1
        ops_count += 1
        logger.debug(
          "Item processed successfully",
          target=target.name,
          type=target.arr_type.value,
          run_id=run_id,
          item_id=item_id_str,
          item_identifier=item_identifier,
          processed=processed,
          ops_count=ops_count,
        )
      except Exception as e:
        logger.warning(
          "Search failed for item",
          target=target.name,
          type=target.arr_type.value,
          run_id=run_id,
          item_id=item_id_str,
          item_identifier=item_identifier,
          error=str(e)[:100],
        )
        request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()
        item_handler.log_error(target.name, item_identifier, e)

    logger.debug(
      "Finished processing items",
      target=target.name,
      type=target.arr_type.value,
      run_id=run_id,
      processed=processed,
      total_items=len(items),
    )
    return processed


class MovieHandler:
  """Handler for processing movies."""

  def extract_id(self, item: dict[str, Any]) -> tuple[int | None, str]:
    """Extract movie ID from item."""
    movie_id = item.get("id")
    return movie_id, f"movie_id={movie_id}" if movie_id is not None else "movie_id=None"

  async def search(self, client: ArrClient, movie_id: int) -> None:
    """Trigger search for a movie."""
    await client.search_movie(movie_id)

  def log_error(self, target_name: str, item_identifier: str, error: Exception) -> None:
    """Log error for movie search."""
    logger.warning(
      "Failed to search movie",
      target=target_name,
      item_identifier=item_identifier,
      error=str(error)[:100],
    )


class SeriesHandler:
  """Handler for processing series."""

  def extract_id(self, item: dict[str, Any]) -> tuple[int | None, str]:
    """Extract series ID from item."""
    series_id = item.get("id")
    return series_id, f"series_id={series_id}" if series_id is not None else "series_id=None"

  async def search(self, client: ArrClient, series_id: int) -> None:
    """Trigger search for a series."""
    await client.search_series(series_id)

  def log_error(self, target_name: str, item_identifier: str, error: Exception) -> None:
    """Log error for series search."""
    logger.warning(
      "Failed to search series",
      target=target_name,
      item_identifier=item_identifier,
      error=str(error)[:100],
    )
