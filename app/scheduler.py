"""Scheduler for periodic search operations."""

import asyncio
import time
from dataclasses import replace
from typing import Any

import structlog

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
from app.handlers import ItemHandler, MovieHandler, SeasonHandler
from app.metrics import (
  grabs_total,
  last_success_timestamp_seconds,
  request_duration_seconds,
  run_total,
  skips_total,
  state_write_failures_total,
)
from app.state import ItemState, ItemStatus, RunStatus, StateManager, TargetState

logger = structlog.get_logger()


def _search_backoff_delay_s(
  consecutive_failures: int,
  initial_s: float,
  exponent: float,
  max_s: float,
) -> float:
  """Compute backoff delay before retrying a failed item (exponential backoff)."""
  if consecutive_failures <= 0:
    return 0.0
  delay = initial_s * (exponent ** (consecutive_failures - 1))
  return min(delay, max_s)


class Scheduler:
  """Schedules and executes periodic search operations.

  The scheduler operates at a high level, working with generic items and delegating
  all item-type-specific operations to ItemHandler implementations. It never needs
  to know about item-type-specific concepts like movie_id, series_id, or season_number.

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
    run_start = time.time()
    duration_s = 0.0

    target_state.last_run_timestamp = run_start
    run_logging_ids = {
      "run_id": f"{target.name}-{int(run_start)}",
      "run_start_timestamp": run_start,
    }
    combined_logging_ids = {**run_logging_ids, **target.logging_ids(), **target_state.logging_ids()}

    logger.debug("Starting run", **combined_logging_ids)

    try:
      client = self.arr_clients[target.name]

      logger.debug("Fetching items", **combined_logging_ids)
      handler: ItemHandler
      if target.arr_type == ArrType.RADARR:
        items = await client.get_movies(combined_logging_ids)
        handler = MovieHandler(target)
      elif target.arr_type == ArrType.SONARR:
        items = await client.get_seasons(combined_logging_ids)
        handler = SeasonHandler(target)
      else:
        raise ValueError(f"Unsupported target type: {target.arr_type}")

      logger.debug(
        "Items fetched",
        item_count=len(items),
        **combined_logging_ids,
      )

      processed = await self._process_items(
        target,
        client,
        items,
        target_state,
        handler,
        run_logging_ids,
      )

      run_end = time.time()

      duration_s = run_end - run_start
      target_state.last_success_timestamp = time.time()
      target_state.last_status = RunStatus.SUCCESS
      target_state.consecutive_failures = 0
      combined_logging_ids.update(target_state.logging_ids())

      last_success_timestamp_seconds.labels(target=target.name, type=target.arr_type.value).set(
        run_end
      )
      run_total.labels(target=target.name, type=target.arr_type.value, status="success").inc()

      logger.debug(
        "Run completed",
        status="success",
        processed=processed,
        duration_s=duration_s,
        **combined_logging_ids,
      )
    except Exception as e:
      duration_s = time.time() - run_start

      target_state.last_status = RunStatus.ERROR
      target_state.consecutive_failures += 1
      combined_logging_ids.update(target_state.logging_ids())

      run_total.labels(target=target.name, type=target.arr_type.value, status="error").inc()

      logger.exception(
        "Run failed",
        exception=e,
        status="error",
        duration_s=duration_s,
        **combined_logging_ids,
      )

    self.state_manager.state.total_runs += 1
    try:
      self.state_manager.save()
    except Exception as e:
      logger.exception("Failed to save state", exception=e)
      state_write_failures_total.inc()

  async def start(self) -> None:
    """Start the scheduler loop."""
    self.running = True
    logger.debug("Scheduler started", targets=len(self.config_targets))

    while self.running:
      tasks = []
      for target in self.config_targets:
        target_state = self.state_manager.get_target_state(target.name)
        if time.time() - target_state.last_run_timestamp >= target.settings.interval_s:
          tasks.append(self.run_once(target))

      if tasks:
        logger.debug("Executing scheduled tasks", task_count=len(tasks))
        await asyncio.gather(*tasks, return_exceptions=True)
      else:
        logger.debug("No tasks to execute, sleeping..")

      await asyncio.sleep(1)

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
    item_handler: ItemHandler,
    logging_ids: dict[str, Any],
  ) -> int:
    """Process items and trigger searches using the provided handler."""
    processed = 0
    ops_count = 0

    # Combine all logging IDs for processing items
    process_logging_ids = {
      **logging_ids,
      **target.logging_ids(),
      **target_state.logging_ids(),
    }

    logger.debug(
      "Processing items",
      total_items=len(items),
      **process_logging_ids,
    )

    for item in items:
      if ops_count >= target.settings.ops_per_interval:
        logger.debug(
          "Reached ops_per_interval limit",
          ops_count=ops_count,
          **process_logging_ids,
        )
        break

      item_logging_ids = {
        **process_logging_ids,
        **item_handler.extract_logging_id(item),
      }
      item_id = item_handler.extract_item_id(item)
      if item_id is None:
        logger.warning("Skipping item with no ID", **item_logging_ids)
        continue

      item_id_str = item_id.format_for_state()
      item_state = target_state.items.get(item_id_str)

      item_logging_ids.update(item_id.logging_ids())
      if item_state is not None:
        item_logging_ids.update(item_state.logging_ids())

      if item_state is not None:
        time_since_last = time.time() - item_state.last_processed_timestamp
        if (
          item_state.last_status == ItemStatus.SUCCESS
          and time_since_last < target.settings.item_revisit_s
        ):
          logger.debug(
            "Skipping item (revisit timeout not met)",
            time_since_last=time_since_last,
            revisit_timeout=target.settings.item_revisit_s,
            **item_logging_ids,
          )
          skips_total.labels(target=target.name, type=target.arr_type.value).inc()
          continue
        if item_state.last_status != ItemStatus.SUCCESS:
          s = target.settings
          if (
            s.search_retry_max_attempts > 0
            and item_state.consecutive_failures >= s.search_retry_max_attempts
          ):
            logger.debug(
              "Skipping item (search retry max attempts exceeded)",
              consecutive_failures=item_state.consecutive_failures,
              search_retry_max_attempts=s.search_retry_max_attempts,
              **item_logging_ids,
            )
            skips_total.labels(target=target.name, type=target.arr_type.value).inc()
            continue
          search_backoff_s = _search_backoff_delay_s(
            item_state.consecutive_failures,
            s.search_retry_initial_delay_s,
            s.search_retry_backoff_exponent,
            s.search_retry_max_delay_s,
          )
          if search_backoff_s > 0 and time_since_last < search_backoff_s:
            logger.debug(
              "Skipping item (search backoff not met)",
              time_since_last=time_since_last,
              search_backoff_s=search_backoff_s,
              consecutive_failures=item_state.consecutive_failures,
              **item_logging_ids,
            )
            skips_total.labels(target=target.name, type=target.arr_type.value).inc()
            continue

      if not item_handler.should_search(item, logging_ids=item_logging_ids):
        skips_total.labels(target=target.name, type=target.arr_type.value).inc()
        continue

      if target.settings.dry_run:
        dry_run_timestamp = time.time()
        if item_state is None:
          dry_run_state = ItemState(
            item_id=item_id_str,
            last_processed_timestamp=dry_run_timestamp,
            last_result="dry_run_search_eligible",
            last_status=ItemStatus.SUCCESS,
            consecutive_failures=0,
          )
        else:
          dry_run_state = replace(
            item_state,
            last_processed_timestamp=dry_run_timestamp,
            last_result="dry_run_search_eligible",
            last_status=ItemStatus.SUCCESS,
            consecutive_failures=0,
          )
        target_state.items[item_id_str] = dry_run_state
        item_state = dry_run_state
        item_logging_ids.update(dry_run_state.logging_ids())

        processed += 1
        ops_count += 1
        logger.debug(
          "Item processed in dry run mode",
          processed=processed,
          ops_count=ops_count,
          **item_logging_ids,
        )
        continue

      try:
        request_start = time.time()
        await item_handler.search(
          client=client,
          item=item,
          logging_ids=process_logging_ids,
        )
        request_end = time.time()
        request_duration = request_end - request_start
        request_duration_seconds.labels(target=target.name, type=target.arr_type.value).observe(
          request_duration
        )

        if item_state is None:
          updated_state = ItemState(
            item_id=item_id_str,
            last_processed_timestamp=request_end,
            last_result="search_triggered",
            last_status=ItemStatus.SUCCESS,
            consecutive_failures=0,
          )
        else:
          updated_state = replace(
            item_state,
            last_processed_timestamp=request_end,
            last_result="search_triggered",
            last_status=ItemStatus.SUCCESS,
            consecutive_failures=0,
          )
        target_state.items[item_id_str] = updated_state
        item_state = updated_state
        item_logging_ids.update(updated_state.logging_ids())

        grabs_total.labels(target=target.name, type=target.arr_type.value).inc()
        processed += 1
        ops_count += 1
        logger.debug(
          "Item processed successfully",
          processed=processed,
          ops_count=ops_count,
          **item_logging_ids,
        )
      except Exception as e:
        error_timestamp = time.time()
        new_failures = (item_state.consecutive_failures + 1) if item_state is not None else 1
        if item_state is None:
          failed_state = ItemState(
            item_id=item_id_str,
            last_processed_timestamp=error_timestamp,
            last_result="search_failed",
            last_status=ItemStatus.ERROR,
            consecutive_failures=new_failures,
          )
        else:
          failed_state = replace(
            item_state,
            last_processed_timestamp=error_timestamp,
            last_result="search_failed",
            last_status=ItemStatus.ERROR,
            consecutive_failures=new_failures,
          )
        target_state.items[item_id_str] = failed_state
        item_state = failed_state
        item_logging_ids.update(failed_state.logging_ids())

        logger.exception(
          "Exception while processing item",
          exception=e,
          **item_logging_ids,
        )

    logger.debug(
      "Finished processing items",
      processed=processed,
      total_items=len(items),
      **process_logging_ids,
    )
    return processed
