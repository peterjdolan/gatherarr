"""Handler for processing individual seasons."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import structlog

from app.action_logging import Action, log_season_action
from app.arr_client import ArrClient
from app.config import ArrTarget
from app.handlers.base import ItemId, _parse_utc_datetime
from app.tag_utils import extract_item_tags, tag_filter

logger = structlog.get_logger()


@dataclass
class SeasonId(ItemId):
  """Item identifier for individual seasons."""

  series_id: int
  season_number: int
  series_name: str | None

  def format_for_state(self) -> str:
    """Format season identity for state lookup."""
    return f"{self.series_id}:{self.season_number}"

  def logging_ids(self) -> dict[str, Any]:
    """Get logging identifiers for the season."""
    return {
      "series_id": str(self.series_id),
      "season_number": str(self.season_number),
      "series_name": self.series_name if self.series_name is not None else "None",
    }


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
