"""Scheduler for periodic search operations."""

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

import structlog

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
from app.logging import Action, log_movie_action, log_series_action
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


def _parse_utc_datetime(value: Any) -> datetime | None:
  """Parse an ISO date/time string into a timezone-aware UTC datetime."""
  if not isinstance(value, str):
    return None

  normalized = value.strip()
  if not normalized:
    return None

  iso_input = f"{normalized[:-1]}+00:00" if normalized.endswith("Z") else normalized
  try:
    parsed = datetime.fromisoformat(iso_input)
  except ValueError:
    return None

  if parsed.tzinfo is None:
    return parsed.replace(tzinfo=timezone.utc)
  return parsed.astimezone(timezone.utc)


def _normalize_item_tags(item: dict[str, Any]) -> set[str]:
  """Extract and normalize item tags for include/exclude filtering."""
  raw_tags = item.get("tags")
  if not isinstance(raw_tags, list):
    return set()

  normalized_tags: set[str] = set()
  for raw_tag in raw_tags:
    normalized_tag = str(raw_tag).strip()
    if normalized_tag:
      normalized_tags.add(normalized_tag)
  return normalized_tags


def _item_matches_tag_filters(
  item: dict[str, Any], include_tags: list[str], exclude_tags: list[str]
) -> bool:
  """Return True if item tags satisfy include/exclude filters."""
  item_tags = _normalize_item_tags(item)

  if include_tags and not any(tag in item_tags for tag in include_tags):
    return False
  if exclude_tags and any(tag in item_tags for tag in exclude_tags):
    return False
  return True


@dataclass
class ItemId:
  """Base class for item identifiers."""

  def format_for_state(self) -> str:
    """Format the item ID for use as a state lookup key."""
    raise NotImplementedError

  def logging_ids(self) -> dict[str, Any]:
    """Get logging identifiers for the item."""
    raise NotImplementedError


@dataclass
class MovieId(ItemId):
  """Item identifier for movies."""

  movie_id: int
  movie_name: str | None

  def format_for_state(self) -> str:
    """Format movie ID for state lookup."""
    return str(self.movie_id)

  def logging_ids(self) -> dict[str, Any]:
    """Get logging identifiers for the movie."""
    return {
      "movie_id": str(self.movie_id),
      "movie_name": self.movie_name if self.movie_name is not None else "None",
    }


@dataclass
class SeriesId(ItemId):
  """Item identifier for series."""

  series_id: int
  series_name: str | None

  def format_for_state(self) -> str:
    """Format series ID and name for state lookup."""
    return str(self.series_id)

  def logging_ids(self) -> dict[str, Any]:
    """Get logging identifiers for the series."""
    return {
      "series_id": str(self.series_id),
      "series_name": self.series_name if self.series_name is not None else "None",
    }


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

  def should_search(self, item: dict[str, Any]) -> bool:
    """Return True when the item meets the handler search criteria."""
    ...

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    logging_ids: dict[str, Any],
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
        items = await client.get_series(combined_logging_ids)
        handler = SeriesHandler(target)
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
      request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()

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
        now = time.time()
        time_since_last = now - target_state.last_run_timestamp

        if time_since_last >= target.interval_s:
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

  @staticmethod
  def _day_start_timestamp(timestamp: float) -> float:
    """Round a timestamp down to the UTC day boundary."""
    seconds_per_day = 86400.0
    return float(int(timestamp // seconds_per_day) * int(seconds_per_day))

  def _is_daily_limit_reached(
    self,
    target: ArrTarget,
    item_state: ItemState | None,
    current_timestamp: float,
  ) -> bool:
    """Return True when max daily searches for an item has been reached."""
    if item_state is None:
      return False
    if target.max_searches_per_item_per_day <= 0:
      return False

    current_day_start = self._day_start_timestamp(current_timestamp)
    if item_state.search_day_start_timestamp != current_day_start:
      return False

    return item_state.search_count_in_day >= target.max_searches_per_item_per_day

  def _build_item_state(
    self,
    item_id: str,
    previous_item_state: ItemState | None,
    processed_timestamp: float,
    last_result: str,
    last_status: str,
    increment_search_count: bool,
  ) -> ItemState:
    """Build the next item state while preserving daily counters."""
    day_start_timestamp = 0.0
    search_count_in_day = 0
    if previous_item_state is not None:
      day_start_timestamp = previous_item_state.search_day_start_timestamp
      search_count_in_day = previous_item_state.search_count_in_day

    if increment_search_count:
      current_day_start = self._day_start_timestamp(processed_timestamp)
      if day_start_timestamp != current_day_start:
        day_start_timestamp = current_day_start
        search_count_in_day = 0
      search_count_in_day += 1

    return ItemState(
      item_id=item_id,
      last_processed_timestamp=processed_timestamp,
      last_result=last_result,
      last_status=last_status,
      search_day_start_timestamp=day_start_timestamp,
      search_count_in_day=search_count_in_day,
    )

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
      if ops_count >= target.ops_per_interval:
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

      now = time.time()
      if item_state is not None:
        time_since_last = now - item_state.last_processed_timestamp
        if item_state.last_status == "success" and time_since_last < target.item_revisit_timeout_s:
          logger.debug(
            "Skipping item (revisit timeout not met)",
            time_since_last=time_since_last,
            revisit_timeout=target.item_revisit_timeout_s,
            **item_logging_ids,
          )
          skips_total.labels(target=target.name, type=target.arr_type.value).inc()
          continue
        if item_state.last_status != "success" and target.search_backoff_s > 0:
          if time_since_last < target.search_backoff_s:
            logger.debug(
              "Skipping item (search backoff not met)",
              time_since_last=time_since_last,
              search_backoff_s=target.search_backoff_s,
              **item_logging_ids,
            )
            skips_total.labels(target=target.name, type=target.arr_type.value).inc()
            continue

      if self._is_daily_limit_reached(target, item_state, now):
        logger.debug(
          "Skipping item (daily search limit reached)",
          max_searches_per_item_per_day=target.max_searches_per_item_per_day,
          **item_logging_ids,
        )
        skips_total.labels(target=target.name, type=target.arr_type.value).inc()
        continue

      if not item_handler.should_search(item):
        logger.debug(
          "Skipping item (search criteria not met)",
          **item_logging_ids,
        )
        skips_total.labels(target=target.name, type=target.arr_type.value).inc()
        continue

      if target.dry_run:
        dry_run_timestamp = time.time()
        dry_run_state = self._build_item_state(
          item_id=item_id_str,
          previous_item_state=item_state,
          processed_timestamp=dry_run_timestamp,
          last_result="dry_run_search_eligible",
          last_status="success",
          increment_search_count=True,
        )
        target_state.items[item_id_str] = dry_run_state
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
        requests_total.labels(target=target.name, type=target.arr_type.value).inc()
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

        item_state = self._build_item_state(
          item_id=item_id_str,
          previous_item_state=item_state,
          processed_timestamp=request_end,
          last_result="search_triggered",
          last_status="success",
          increment_search_count=True,
        )
        target_state.items[item_id_str] = item_state
        item_logging_ids.update(item_state.logging_ids())

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
        failed_state = self._build_item_state(
          item_id=item_id_str,
          previous_item_state=item_state,
          processed_timestamp=error_timestamp,
          last_result="search_failed",
          last_status="error",
          increment_search_count=True,
        )
        target_state.items[item_id_str] = failed_state
        item_logging_ids.update(failed_state.logging_ids())

        logger.exception(
          "Exception while processing item",
          exception=e,
          **item_logging_ids,
        )
        request_errors_total.labels(target=target.name, type=target.arr_type.value).inc()

    logger.debug(
      "Finished processing items",
      processed=processed,
      total_items=len(items),
      **process_logging_ids,
    )
    return processed


class MovieHandler:
  """Handler for processing movies."""

  def __init__(self, target: ArrTarget) -> None:
    self.target = target

  def should_search(self, item: dict[str, Any]) -> bool:
    """Return True when movie satisfies configured eligibility rules."""
    if self.target.require_monitored and item.get("monitored") is not True:
      return False
    if self.target.require_cutoff_unmet and not self._is_cutoff_unmet(item):
      return False
    if not _item_matches_tag_filters(item, self.target.include_tags, self.target.exclude_tags):
      return False
    if self.target.released_only and not self._is_released(item):
      return False
    return True

  def _is_cutoff_unmet(self, item: dict[str, Any]) -> bool:
    """Determine whether Radarr quality cutoff has not been reached."""
    movie_file = item.get("movieFile")
    if isinstance(movie_file, dict):
      quality_cutoff_not_met = movie_file.get("qualityCutoffNotMet")
      if isinstance(quality_cutoff_not_met, bool):
        return quality_cutoff_not_met

    has_file = item.get("hasFile")
    if isinstance(has_file, bool):
      return not has_file

    return False

  def _is_released(self, item: dict[str, Any]) -> bool:
    """Determine whether a movie has reached release availability."""
    if item.get("hasFile") is True:
      return True

    now = datetime.now(timezone.utc)
    release_keys = ("digitalRelease", "physicalRelease", "inCinemas")
    for key in release_keys:
      release_dt = _parse_utc_datetime(item.get(key))
      if release_dt is not None and release_dt <= now:
        return True
    return False

  def extract_item_id(self, item: dict[str, Any]) -> MovieId | None:
    """Extract item ID for state tracking."""
    movie_id = item.get("id")
    if movie_id is None:
      return None

    movie_name = item.get("title")
    return MovieId(movie_id=movie_id, movie_name=movie_name)

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers."""
    item_id = self.extract_item_id(item)
    if item_id is None:
      return {}

    movie_id = item_id.movie_id
    movie_name = item.get("title")

    return {
      "movie_id": str(movie_id),
      "movie_name": movie_name if movie_name is not None else "None",
    }

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    logging_ids: dict[str, Any],
  ) -> None:
    """Trigger search for a movie and log the action."""

    item_id = self.extract_item_id(item)
    if item_id is None:
      raise ValueError("Movie ID is required")

    item_logging_ids = self.extract_logging_id(item)
    combined_logging_ids = {**logging_ids, **item_logging_ids}
    await client.search_movie(item_id, logging_ids=combined_logging_ids)

    log_movie_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      movie_id=item_id,
      **logging_ids,
    )


class SeriesHandler:
  """Handler for processing series.

  This handler is responsible for extracting the item ID and logging identifiers for series.
  It also triggers the search for the series and logs the action. It is used to handle series-wide
  searches, but not season-specific or episode-specific searches.
  """

  def __init__(self, target: ArrTarget) -> None:
    self.target = target

  def should_search(self, item: dict[str, Any]) -> bool:
    """Return True when series satisfies configured eligibility rules."""
    if self.target.require_monitored and item.get("monitored") is not True:
      return False
    if self.target.require_cutoff_unmet and not self._is_cutoff_unmet(item):
      return False
    if not _item_matches_tag_filters(item, self.target.include_tags, self.target.exclude_tags):
      return False
    if self.target.released_only and not self._is_released(item):
      return False
    if not self._meets_missing_thresholds(item):
      return False
    return True

  def _is_cutoff_unmet(self, item: dict[str, Any]) -> bool:
    """Determine whether Sonarr quality cutoff has not been reached."""
    statistics = item.get("statistics")
    if not isinstance(statistics, dict):
      return False

    quality_cutoff_not_met = statistics.get("qualityCutoffNotMet")
    if isinstance(quality_cutoff_not_met, bool):
      return quality_cutoff_not_met

    episode_file_count = statistics.get("episodeFileCount")
    total_episode_count = statistics.get("totalEpisodeCount")
    if (
      isinstance(episode_file_count, int)
      and not isinstance(episode_file_count, bool)
      and isinstance(total_episode_count, int)
      and not isinstance(total_episode_count, bool)
    ):
      return episode_file_count < total_episode_count

    percent_of_episodes = statistics.get("percentOfEpisodes")
    if isinstance(percent_of_episodes, float):
      return percent_of_episodes < 100.0
    if isinstance(percent_of_episodes, int) and not isinstance(percent_of_episodes, bool):
      return percent_of_episodes < 100

    return False

  def _is_released(self, item: dict[str, Any]) -> bool:
    """Determine whether a series has released episodes."""
    now = datetime.now(timezone.utc)
    first_aired = _parse_utc_datetime(item.get("firstAired"))
    if first_aired is not None and first_aired <= now:
      return True

    statistics = item.get("statistics")
    if not isinstance(statistics, dict):
      return False
    episode_file_count = statistics.get("episodeFileCount")
    if isinstance(episode_file_count, int) and not isinstance(episode_file_count, bool):
      return episode_file_count > 0
    return False

  def _meets_missing_thresholds(self, item: dict[str, Any]) -> bool:
    """Validate configured series missing-episode thresholds."""
    if self.target.min_missing_episodes <= 0 and self.target.min_missing_percent <= 0:
      return True

    statistics = item.get("statistics")
    if not isinstance(statistics, dict):
      return False

    missing_episode_count = self._missing_episode_count(statistics)
    if self.target.min_missing_episodes > 0:
      if missing_episode_count is None:
        return False
      if missing_episode_count < self.target.min_missing_episodes:
        return False

    missing_percent = self._missing_percent(statistics, missing_episode_count)
    if self.target.min_missing_percent > 0:
      if missing_percent is None:
        return False
      if missing_percent < self.target.min_missing_percent:
        return False

    return True

  def _missing_episode_count(self, statistics: dict[str, Any]) -> int | None:
    """Calculate missing episodes from statistics counters."""
    episode_file_count = statistics.get("episodeFileCount")
    total_episode_count = statistics.get("totalEpisodeCount")
    if (
      isinstance(episode_file_count, int)
      and not isinstance(episode_file_count, bool)
      and isinstance(total_episode_count, int)
      and not isinstance(total_episode_count, bool)
    ):
      return max(total_episode_count - episode_file_count, 0)
    return None

  def _missing_percent(
    self, statistics: dict[str, Any], missing_episode_count: int | None
  ) -> float | None:
    """Calculate missing percent from statistics counters."""
    percent_of_episodes = statistics.get("percentOfEpisodes")
    if isinstance(percent_of_episodes, float):
      return max(100.0 - percent_of_episodes, 0.0)
    if isinstance(percent_of_episodes, int) and not isinstance(percent_of_episodes, bool):
      return max(100.0 - float(percent_of_episodes), 0.0)

    total_episode_count = statistics.get("totalEpisodeCount")
    if (
      missing_episode_count is not None
      and isinstance(total_episode_count, int)
      and not isinstance(total_episode_count, bool)
      and total_episode_count > 0
    ):
      return (missing_episode_count / total_episode_count) * 100.0
    return None

  def extract_item_id(self, item: dict[str, Any]) -> SeriesId | None:
    """Extract item ID for state tracking."""
    series_id = item.get("id")
    if series_id is None:
      return None

    series_name = item.get("title")
    return SeriesId(series_id=series_id, series_name=series_name)

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers."""
    item_id = self.extract_item_id(item)
    if item_id is None:
      return {}

    series_name = item.get("title")

    return {
      "series_id": str(item_id.series_id),
      "series_name": series_name if series_name is not None else "None",
    }

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    logging_ids: dict[str, Any],
  ) -> None:
    """Trigger search for a series and log the action."""

    series_id = self.extract_item_id(item)
    if series_id is None:
      raise ValueError("Series ID is required")

    item_logging_ids = self.extract_logging_id(item)
    combined_logging_ids = {**logging_ids, **item_logging_ids}
    await client.search_series(series_id, logging_ids=combined_logging_ids)

    log_series_action(
      logger=logger,
      action=Action.SEARCH_SERIES,
      series_id=series_id,
      **logging_ids,
    )
