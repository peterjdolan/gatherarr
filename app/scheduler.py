"""Scheduler for periodic search operations."""

import asyncio
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, Protocol

import structlog
from dateutil import parser as dateutil_parser

from app.action_logging import Action, log_movie_action, log_season_action
from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
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
from app.state import ItemState, ItemStatus, RunStatus, StateManager, TargetState
from app.tag_utils import extract_item_tags, tag_filter

logger = structlog.get_logger()


def _parse_utc_datetime(value: Any) -> datetime | None:
  """Parse a date/time string into a timezone-aware UTC datetime."""
  if not isinstance(value, str):
    return None

  normalized = value.strip()
  if not normalized:
    return None

  try:
    parsed = dateutil_parser.parse(normalized)
  except ValueError, TypeError:
    return None

  if parsed.tzinfo is None:
    return parsed.replace(tzinfo=timezone.utc)
  return parsed.astimezone(timezone.utc)


@dataclass
class ItemId:
  """Base class for item identifiers."""

  def format_for_state(self) -> str:
    """Format the item ID for use as a state lookup key."""
    raise NotImplementedError

  def logging_ids(self) -> dict[str, str]:
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

  def logging_ids(self) -> dict[str, str]:
    """Get logging identifiers for the movie."""
    return {
      "movie_id": str(self.movie_id),
      "movie_name": self.movie_name if self.movie_name is not None else "None",
    }


@dataclass
class SeasonId(ItemId):
  """Item identifier for individual seasons."""

  series_id: int
  season_number: int
  series_name: str | None

  def format_for_state(self) -> str:
    """Format season identity for state lookup."""
    return f"{self.series_id}:{self.season_number}"

  def logging_ids(self) -> dict[str, str]:
    """Get logging identifiers for the season."""
    return {
      "series_id": str(self.series_id),
      "season_number": str(self.season_number),
      "series_name": self.series_name if self.series_name is not None else "None",
    }


class ItemHandler(Protocol):
  """Protocol for handling individual items.

  The ItemHandler abstracts away item-type-specific details (such as movie_id, series_id,
  season_number) from the scheduler. The scheduler works with generic items and delegates
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

  def should_search(self, item: dict[str, Any], logging_ids: dict[str, Any]) -> bool:
    """Return True when the item meets the handler search criteria.

    Args:
      item: The item to check eligibility for.
      logging_ids: Logging context for debug messages.
    """
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
        if item_state.last_status != ItemStatus.SUCCESS and target.settings.search_backoff_s > 0:
          if time_since_last < target.settings.search_backoff_s:
            logger.debug(
              "Skipping item (search backoff not met)",
              time_since_last=time_since_last,
              search_backoff_s=target.settings.search_backoff_s,
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
          )
        else:
          dry_run_state = replace(
            item_state,
            last_processed_timestamp=dry_run_timestamp,
            last_result="dry_run_search_eligible",
            last_status=ItemStatus.SUCCESS,
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

        if item_state is None:
          updated_state = ItemState(
            item_id=item_id_str,
            last_processed_timestamp=request_end,
            last_result="search_triggered",
            last_status=ItemStatus.SUCCESS,
          )
        else:
          updated_state = replace(
            item_state,
            last_processed_timestamp=request_end,
            last_result="search_triggered",
            last_status=ItemStatus.SUCCESS,
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
        if item_state is None:
          failed_state = ItemState(
            item_id=item_id_str,
            last_processed_timestamp=error_timestamp,
            last_result="search_failed",
            last_status=ItemStatus.ERROR,
          )
        else:
          failed_state = replace(
            item_state,
            last_processed_timestamp=error_timestamp,
            last_result="search_failed",
            last_status=ItemStatus.ERROR,
          )
        target_state.items[item_id_str] = failed_state
        item_state = failed_state
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

  def should_search(self, item: dict[str, Any], logging_ids: dict[str, Any]) -> bool:
    """Return True when movie satisfies configured eligibility rules."""
    if self.target.settings.require_monitored and item.get("monitored") is not True:
      logger.debug(
        "Skipping movie (not monitored)",
        require_monitored=self.target.settings.require_monitored,
        monitored=item.get("monitored"),
        **logging_ids,
      )
      return False
    if self.target.settings.require_cutoff_unmet and not self._is_cutoff_unmet(item):
      logger.debug(
        "Skipping movie (quality cutoff met)",
        require_cutoff_unmet=self.target.settings.require_cutoff_unmet,
        has_file=item.get("hasFile"),
        **logging_ids,
      )
      return False
    item_tags = extract_item_tags(item)
    if not tag_filter(
      item_tags,
      self.target.settings.include_tags,
      self.target.settings.exclude_tags,
    ):
      logger.debug(
        "Skipping movie (tag filter not met)",
        item_tags=sorted(item_tags) if item_tags else [],
        include_tags=sorted(self.target.settings.include_tags)
        if self.target.settings.include_tags
        else [],
        exclude_tags=sorted(self.target.settings.exclude_tags)
        if self.target.settings.exclude_tags
        else [],
        **logging_ids,
      )
      return False
    if self.target.settings.released_only and not self._is_released(item):
      logger.debug(
        "Skipping movie (not released)",
        released_only=self.target.settings.released_only,
        has_file=item.get("hasFile"),
        **logging_ids,
      )
      return False
    return True

  def _is_cutoff_unmet(self, item: dict[str, Any]) -> bool:
    """Determine whether Radarr quality cutoff has not been reached."""
    movie_file = item.get("movieFile")
    if movie_file is not None:
      quality_cutoff_not_met = movie_file.get("qualityCutoffNotMet")
      return quality_cutoff_not_met is True

    has_file = item.get("hasFile")
    return has_file is False

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


class SeasonHandler:
  """Handler for processing individual seasons."""

  def __init__(self, target: ArrTarget) -> None:
    self.target = target

  def extract_item_id(self, item: dict[str, Any]) -> SeasonId | None:
    """Extract season ID for state tracking."""
    series_id = item.get("seriesId")
    season_number = item.get("seasonNumber")
    if series_id is None or season_number is None:
      return None

    series_name = item.get("seriesTitle")
    return SeasonId(series_id=series_id, season_number=season_number, series_name=series_name)

  def extract_logging_id(self, item: dict[str, Any]) -> dict[str, str]:
    """Extract logging identifiers."""
    item_id = self.extract_item_id(item)
    if item_id is None:
      return {}

    return {
      "series_id": str(item_id.series_id),
      "season_number": str(item_id.season_number),
      "series_name": item_id.series_name if item_id.series_name is not None else "None",
    }

  def should_search(self, item: dict[str, Any], logging_ids: dict[str, Any]) -> bool:
    """Return True when season satisfies configured eligibility rules."""
    # Check series-level monitored status
    if self.target.settings.require_monitored:
      series_monitored = item.get("seriesMonitored")
      season_monitored = item.get("seasonMonitored")
      # Season must be monitored, and if series monitoring is available, series should be monitored too
      if season_monitored is not True:
        logger.debug(
          "Skipping season (season not monitored)",
          require_monitored=self.target.settings.require_monitored,
          season_monitored=season_monitored,
          **logging_ids,
        )
        return False
      if series_monitored is not None and series_monitored is not True:
        logger.debug(
          "Skipping season (series not monitored)",
          require_monitored=self.target.settings.require_monitored,
          series_monitored=series_monitored,
          **logging_ids,
        )
        return False

    # Check cutoff unmet status
    if self.target.settings.require_cutoff_unmet and not self._is_cutoff_unmet(item):
      logger.debug(
        "Skipping season (quality cutoff met)",
        require_cutoff_unmet=self.target.settings.require_cutoff_unmet,
        **logging_ids,
      )
      return False

    # Check tag filters (using series tags)
    series_tags = item.get("seriesTags")
    item_tags = extract_item_tags({"tags": series_tags})
    if not tag_filter(
      item_tags,
      self.target.settings.include_tags,
      self.target.settings.exclude_tags,
    ):
      logger.debug(
        "Skipping season (tag filter not met)",
        item_tags=sorted(item_tags) if item_tags else [],
        include_tags=sorted(self.target.settings.include_tags)
        if self.target.settings.include_tags
        else [],
        exclude_tags=sorted(self.target.settings.exclude_tags)
        if self.target.settings.exclude_tags
        else [],
        **logging_ids,
      )
      return False

    # Check released status
    if self.target.settings.released_only and not self._is_released(item):
      logger.debug(
        "Skipping season (not released)",
        released_only=self.target.settings.released_only,
        **logging_ids,
      )
      return False

    # Check missing episode thresholds
    if not self._meets_missing_thresholds(item, logging_ids):
      return False

    return True

  def _is_cutoff_unmet(self, item: dict[str, Any]) -> bool:
    """Determine whether season quality cutoff has not been reached."""
    season_statistics = item.get("seasonStatistics")
    if season_statistics is not None:
      episode_file_count = season_statistics.get("episodeFileCount")
      episode_count = season_statistics.get("episodeCount")
      total_episode_count = season_statistics.get("totalEpisodeCount")
      if episode_file_count is not None and total_episode_count is not None:
        return bool(episode_file_count < total_episode_count)
      if episode_file_count is not None and episode_count is not None:
        return bool(episode_file_count < episode_count)

      percent_of_episodes = season_statistics.get("percentOfEpisodes")
      if percent_of_episodes is not None:
        return float(percent_of_episodes) < 100.0

    # Fallback to series-level statistics if season statistics unavailable
    series_statistics = item.get("seriesStatistics")
    if series_statistics is not None:
      quality_cutoff_not_met = series_statistics.get("qualityCutoffNotMet")
      return quality_cutoff_not_met is True

    return False

  def _is_released(self, item: dict[str, Any]) -> bool:
    """Determine whether a season has released episodes."""
    season_statistics = item.get("seasonStatistics")
    if season_statistics is not None:
      episode_file_count = season_statistics.get("episodeFileCount")
      if episode_file_count is not None:
        return bool(episode_file_count > 0)

      previous_airing = season_statistics.get("previousAiring")
      if previous_airing is not None:
        now = datetime.now(timezone.utc)
        airing_dt = _parse_utc_datetime(previous_airing)
        if airing_dt is not None and airing_dt <= now:
          return True

    # Fallback to series first aired
    series_first_aired = item.get("seriesFirstAired")
    if series_first_aired is not None:
      now = datetime.now(timezone.utc)
      first_aired = _parse_utc_datetime(series_first_aired)
      if first_aired is not None and first_aired <= now:
        return True

    return False

  def _meets_missing_thresholds(self, item: dict[str, Any], logging_ids: dict[str, Any]) -> bool:
    """Validate configured season missing-episode thresholds."""
    if (
      self.target.settings.min_missing_episodes <= 0
      and self.target.settings.min_missing_percent <= 0
    ):
      return True

    season_statistics = item.get("seasonStatistics")
    if season_statistics is None:
      logger.debug(
        "Skipping season (missing season statistics for threshold check)",
        min_missing_episodes=self.target.settings.min_missing_episodes,
        min_missing_percent=self.target.settings.min_missing_percent,
        **logging_ids,
      )
      return False

    missing_episode_count = self._missing_episode_count(season_statistics)
    if self.target.settings.min_missing_episodes > 0:
      if missing_episode_count is None:
        logger.debug(
          "Skipping season (cannot determine missing episode count)",
          min_missing_episodes=self.target.settings.min_missing_episodes,
          **logging_ids,
        )
        return False
      if missing_episode_count < self.target.settings.min_missing_episodes:
        logger.debug(
          "Skipping season (missing episode count below threshold)",
          missing_episode_count=missing_episode_count,
          min_missing_episodes=self.target.settings.min_missing_episodes,
          **logging_ids,
        )
        return False

    missing_percent = self._missing_percent(season_statistics, missing_episode_count)
    if self.target.settings.min_missing_percent > 0:
      if missing_percent is None:
        logger.debug(
          "Skipping season (cannot determine missing episode percent)",
          min_missing_percent=self.target.settings.min_missing_percent,
          **logging_ids,
        )
        return False
      if missing_percent < self.target.settings.min_missing_percent:
        logger.debug(
          "Skipping season (missing episode percent below threshold)",
          missing_percent=missing_percent,
          min_missing_percent=self.target.settings.min_missing_percent,
          **logging_ids,
        )
        return False

    return True

  def _missing_episode_count(self, statistics: dict[str, Any]) -> int | None:
    """Calculate missing episodes from season statistics counters."""
    episode_file_count = statistics.get("episodeFileCount")
    total_episode_count = statistics.get("totalEpisodeCount")
    if episode_file_count is not None and total_episode_count is not None:
      return int(max(total_episode_count - episode_file_count, 0))

    episode_count = statistics.get("episodeCount")
    if episode_file_count is not None and episode_count is not None:
      return int(max(episode_count - episode_file_count, 0))

    return None

  def _missing_percent(
    self, statistics: dict[str, Any], missing_episode_count: int | None
  ) -> float | None:
    """Calculate missing percent from season statistics counters."""
    percent_of_episodes = statistics.get("percentOfEpisodes")
    if percent_of_episodes is not None:
      return max(100.0 - float(percent_of_episodes), 0.0)

    total_episode_count = statistics.get("totalEpisodeCount")
    if (
      missing_episode_count is not None
      and total_episode_count is not None
      and total_episode_count > 0
    ):
      return float((missing_episode_count / total_episode_count) * 100.0)

    episode_count = statistics.get("episodeCount")
    if missing_episode_count is not None and episode_count is not None and episode_count > 0:
      return float((missing_episode_count / episode_count) * 100.0)

    return None

  async def search(
    self,
    client: ArrClient,
    item: dict[str, Any],
    logging_ids: dict[str, Any],
  ) -> None:
    """Trigger search for a season and log the action."""

    season_id = self.extract_item_id(item)
    if season_id is None:
      raise ValueError("Season ID is required")

    item_logging_ids = self.extract_logging_id(item)
    combined_logging_ids = {**logging_ids, **item_logging_ids}
    await client.search_season(season_id, logging_ids=combined_logging_ids)

    log_season_action(
      logger=logger,
      action=Action.SEARCH_SEASON,
      season_id=season_id,
      **logging_ids,
    )
