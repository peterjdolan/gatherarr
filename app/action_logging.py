"""Helper functions for consistent item-related logging with correlation fields."""

from enum import StrEnum
from typing import TYPE_CHECKING, Any

import structlog

if TYPE_CHECKING:
  from app.handlers import ItemId, MovieId, SeasonId


class Action(StrEnum):
  """Actions that can be logged."""

  GET_MOVIES = "get_movies"
  GET_SEASONS = "get_seasons"
  SEARCH_MOVIE = "search_movie"
  SEARCH_SEASON = "search_season"


def log_item_action(
  logger: structlog.BoundLogger,
  action: Action,
  item_id: "ItemId",
  **kwargs: Any,
) -> None:
  """Helper function to log an item-related action with correlation fields at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    **kwargs: Additional fields to include in the log entry (e.g., run_id, target_name, arr_type, movie_id, series_id, season_number)
  """
  logger.info(
    f"Action: {action.value}",
    action=action.value,
    **kwargs,
    **item_id.logging_ids(),
  )


def log_movie_action(
  logger: structlog.BoundLogger,
  action: Action,
  movie_id: "MovieId",
  **kwargs: Any,
) -> None:
  """Log a movie-related action with required movie_id correlation field at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    movie_id: Movie identifier
    **kwargs: Additional fields to include in the log entry
  """
  log_item_action(
    logger=logger,
    action=action,
    item_id=movie_id,
    **kwargs,
  )


def log_season_action(
  logger: structlog.BoundLogger,
  action: Action,
  season_id: "SeasonId",
  **kwargs: Any,
) -> None:
  """Log a season-related action with required season correlation fields at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    season_id: Season identifier (series + season number)
    **kwargs: Additional fields to include in the log entry
  """
  log_item_action(
    logger=logger,
    action=action,
    item_id=season_id,
    **kwargs,
  )
