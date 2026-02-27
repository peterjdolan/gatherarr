"""Base types and utilities for item handlers."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from dateutil import parser as dateutil_parser


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
    client: Any,
    item: dict[str, Any],
    logging_ids: dict[str, Any],
  ) -> None:
    """Trigger search for the item and log the action."""
    ...
