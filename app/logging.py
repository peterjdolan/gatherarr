"""Helper functions for consistent item-related logging with correlation fields."""

from typing import Any

import structlog


def log_item_action(
  logger: structlog.BoundLogger,
  action: str,
  **kwargs: Any,
) -> None:
  """Helper function to log an item-related action with correlation fields at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    **kwargs: Additional fields to include in the log entry (e.g., run_id, target_name, arr_type, movie_id, series_id, season_id)
  """
  logger.info(action=action, **kwargs)


def log_movie_action(
  logger: structlog.BoundLogger,
  action: str,
  movie_id: int,
  movie_name: str | None = None,
  **kwargs: Any,
) -> None:
  """Log a movie-related action with required movie_id correlation field at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    movie_id: Movie identifier (required correlation field)
    movie_name: Optional movie name for readability
    **kwargs: Additional fields to include in the log entry
  """
  log_data = {"movie_id": movie_id, **kwargs}
  if movie_name is not None:
    log_data["movie_name"] = movie_name

  log_item_action(
    logger=logger,
    action=action,
    **log_data,
  )


def log_series_action(
  logger: structlog.BoundLogger,
  action: str,
  series_id: int,
  series_name: str | None = None,
  **kwargs: Any,
) -> None:
  """Log a series-related action with required series_id and season_id correlation fields at INFO level.

  Args:
    logger: The structlog logger instance to use
    action: Action description/message
    series_id: Series identifier (required correlation field)
    series_name: Optional series name for readability
    **kwargs: Additional fields to include in the log entry
  """
  log_data = {
    "series_id": series_id,
    **kwargs,
  }
  if series_name is not None:
    log_data["series_name"] = series_name

  log_item_action(
    logger=logger,
    action=action,
    **log_data,
  )
