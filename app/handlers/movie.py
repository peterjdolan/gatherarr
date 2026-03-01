"""Handler for processing movies."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import structlog

from app.action_logging import Action, log_movie_action
from app.arr_client import ArrClient
from app.config import ArrTarget
from app.handlers.base import ItemId, _parse_utc_datetime
from app.tag_utils import extract_item_tags, tag_filter

logger = structlog.get_logger()


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
    if self.target.settings.require_released and not self._is_released(item):
      logger.debug(
        "Skipping movie (not released)",
        require_released=self.target.settings.require_released,
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
