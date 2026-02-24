"""Scheduler for periodic search operations."""

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Protocol

import structlog

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
from app.logging import log_movie_action, log_series_action
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


@dataclass
class ItemId:
  """Base class for item identifiers."""

  def format_for_state(self) -> str:
    """Format the item ID for use as a state lookup key."""
    raise NotImplementedError


@dataclass
class MovieId(ItemId):
  """Item identifier for movies."""

  movie_id: int

  def format_for_state(self) -> str:
    """Format movie ID for state lookup."""
    return str(self.movie_id)


@dataclass
class SeriesId(ItemId):
  """Item identifier for series."""

  series_id: int

  def format_for_state(self) -> str:
    """Format series ID for state lookup."""
    return str(self.series_id)


class ItemHandler(Protocol):
  """Protocol for handling individual items.

  The ItemHandler abstracts away item-type-specific details (such as movie_id, series_id,
  season_id) from the scheduler. The scheduler works with generic items and delegates
  all item-type-specific operations (ID extraction, logging, searching) to the handler.

  This separation ensures the scheduler never needs to know about item-type-specific
  concepts like movies, series, or seasons - it only deals with generic items and
  their handlers.
  """

  def extract_item_id(self, item: dict[str, Any]) -> ItemId | None:
    """Extract item ID for use in revisit timing calculations.

    Returns:
      ItemId instance containing the item identifier(s) needed for state tracking.
      Returns None if the item has no valid ID.
    """
    ...

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers for use in log messages.

    Returns:
      Dictionary containing string values that can be passed as kwargs to log messages.
    """
    ...

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    target: ArrTarget,
    logging_ids: dict[str, str],
  ) -> None:
    """Trigger search for the item and log the action."""
    ...


class Scheduler:
  """Schedules and executes periodic search operations.

  The scheduler operates at a high level, working with generic items and delegating
  all item-type-specific operations to ItemHandler implementations. It never needs
  to know about item-type-specific concepts like movie_id, series_id, or season_id.

  All item identification, logging format, and search operations are abstracted
  through the ItemHandler protocol, ensuring a clean separation of concerns.
  """

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
    logging_ids = {
      "target_name": target.name,
      "target_type": target.arr_type.value,
      "run_id": run_id,
    }

    logger.debug(
      "Starting run",
      ops_per_interval=target.ops_per_interval,
      interval_s=target.interval_s,
      item_revisit_timeout_s=target.item_revisit_timeout_s,
      **logging_ids,
    )

    try:
      client = self.arr_clients[target.name]
      start_time = time.time()

      logger.debug(
        "Fetching items",
        **logging_ids,
      )
      if target.arr_type == ArrType.RADARR:
        items = await client.get_movies()
        handler: ItemHandler = MovieHandler()
      elif target.arr_type == ArrType.SONARR:
        items = await client.get_series()
        handler = SeriesHandler()
      else:
        raise ValueError(f"Unsupported target type: {target.arr_type}")

      logger.debug(
        "Items fetched",
        item_count=len(items),
        **logging_ids,
      )

      processed = await self._process_items(
        target, client, items, target_state, now, run_id, handler
      )

      duration_ms = int((time.time() - start_time) * 1000)
      target_state.last_success_timestamp = now
      target_state.last_status = RunStatus.SUCCESS
      target_state.consecutive_failures = 0

      last_success_timestamp_seconds.labels(target=target.name, type=target.arr_type.value).set(now)
      run_total.labels(target=target.name, type=target.arr_type.value, status="success").inc()

      logger.debug(
        "Run completed",
        status="success",
        processed=processed,
        duration_ms=duration_ms,
        target_state=target_state,
        **logging_ids,
      )
    except Exception as e:
      error_msg = str(e)[:200]
      target_state.last_status = RunStatus.ERROR
      target_state.consecutive_failures += 1

      run_total.labels(target=target.name, type=target.arr_type.value, status="error").inc()
      request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()

      logger.error(
        "Run failed",
        status="error",
        error=error_msg,
        duration_ms=duration_ms,
        target_state=target_state,
        **logging_ids,
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
    logger.debug("Scheduler started", targets=len(self.config_targets))

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
    logger.debug("Scheduler stopped")

  async def _process_items(
    self,
    target: ArrTarget,
    client: ArrClient,
    items: list[dict[str, Any]],
    target_state: TargetState,
    now: float,
    logging_ids: dict[str, str],
    item_handler: ItemHandler,
  ) -> int:
    """Process items and trigger searches using the provided handler."""
    processed = 0
    ops_count = 0

    logger.debug(
      "Processing items",
      target_name=target.name,
      target_type=target.arr_type.value,
      total_items=len(items),
      ops_per_interval=target.ops_per_interval,
      **logging_ids,
    )

    for item in items:
      if ops_count >= target.ops_per_interval:
        logger.debug(
          "Reached ops_per_interval limit",
          target_name=target.name,
          target_type=target.arr_type.value,
          ops_count=ops_count,
          ops_per_interval=target.ops_per_interval,
          **logging_ids,
        )
        break

      logging_ids = item_handler.extract_logging_id(item)
      item_id = item_handler.extract_item_id(item)
      if item_id is None:
        # Use generic logger for items without IDs since we don't have correlation fields
        logger.warning(
          "Skipping item with no ID",
          target_name=target.name,
          target_type=target.arr_type.value,
          **logging_ids,
        )
        continue

      item_id_str = item_id.format_for_state()
      item_state = target_state.items.get(item_id_str)

      if item_state is not None:
        time_since_last = now - item_state.last_processed_timestamp
        if time_since_last < target.item_revisit_timeout_s:
          logger.debug(
            "Skipping item (revisit timeout not met)",
            target=target.name,
            type=target.arr_type.value,
            time_since_last=time_since_last,
            revisit_timeout=target.item_revisit_timeout_s,
            **logging_ids,
          )
          skips_total.labels(target=target.name, type=target.arr_type.value).inc()
          continue

      try:
        request_start = time.time()
        requests_total.labels(target=target.name, type=target.arr_type.value).inc()
        await item_handler.search(
          client=client,
          item=item,
          target=target,
          logging_ids=logging_ids,
        )
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
          target_name=target.name,
          target_type=target.arr_type.value,
          processed=processed,
          ops_count=ops_count,
          **logging_ids,
        )
      except Exception as e:
        logger.warning(
          "Search failed for item",
          target_name=target.name,
          target_type=target.arr_type.value,
          error=str(e)[:100],
          **logging_ids,
        )
        request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()

    logger.debug(
      "Finished processing items",
      target=target.name,
      type=target.arr_type.value,
      processed=processed,
      total_items=len(items),
      **logging_ids,
    )
    return processed


class MovieHandler:
  """Handler for processing movies."""

  def extract_item_id(self, item: dict[str, Any]) -> ItemId | None:
    """Extract item ID for state tracking."""
    movie_id = item.get("id")
    if movie_id is None:
      return None
    return MovieId(movie_id=movie_id)

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers."""
    movie_id = item.get("id")
    return {
      "movie_id": str(movie_id) if movie_id is not None else "",
      "item_identifier": f"movie_id={movie_id}" if movie_id is not None else "movie_id=None",
    }

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    target: ArrTarget,
    run_id: str,
  ) -> None:
    """Trigger search for a movie and log the action."""

    movie_id = item.get("id")
    if movie_id is None:
      raise ValueError("Movie ID is required")

    logging_ids = self.extract_logging_id(item)
    log_movie_action(
      logger=logger,
      action="Triggering search for item",
      movie_id=int(logging_ids["movie_id"]),
      target_name=target.name,
      arr_type=target.arr_type,
      run_id=run_id,
      movie_name=item.get("title"),
      item_identifier=logging_ids.get("item_identifier"),
    )
    await client.search_movie(movie_id)


class SeriesHandler:
  """Handler for processing series.

  This handler is responsible for extracting the item ID and logging identifiers for series.
  It also triggers the search for the series and logs the action. It is used to handle series-wide
  searches, but not season-specific or episode-specific searches.
  """

  def extract_item_id(self, item: dict[str, Any]) -> ItemId | None:
    """Extract item ID for state tracking."""
    series_id = item.get("id")
    if series_id is None:
      return None

    return SeriesId(series_id=series_id)

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers."""
    id = self.extract_item_id(item)
    if id is None:
      return {}
    return {
      "series_id": str(id.series_id),
    }

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    target: ArrTarget,
    run_id: str,
  ) -> None:
    """Trigger search for a series and log the action."""
    series_id = item.get("id")
    if series_id is None:
      raise ValueError("Series ID is required")
    # For series-wide searches, season_id is None
    # If we need season-specific operations in the future, extract from item data
    season_id: int | None = None

    logging_ids = self.extract_logging_id(item)
    log_series_action(
      logger=logger,
      action="Triggering search for item",
      series_id=int(logging_ids["series_id"]),
      season_id=season_id,
      target_name=target.name,
      arr_type=target.arr_type,
      run_id=run_id,
      series_name=item.get("title"),
      item_identifier=logging_ids.get("item_identifier"),
    )
    await client.search_series(series_id, season_id=season_id)
