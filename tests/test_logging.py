"""Tests for logging module."""

from unittest.mock import Mock

import structlog

from app.config import ArrType
from app.logging import Action, log_item_action, log_movie_action, log_series_action
from app.scheduler import MovieId


class TestLogging:
  def test_log_item_action(self) -> None:
    """Test log_item_action logs with all provided fields at INFO level."""
    mock_info = Mock()
    logger = Mock(spec=structlog.BoundLogger)
    logger.info = mock_info

    movie_id = MovieId(movie_id=42, movie_name="Test Movie")
    log_item_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      item_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    mock_info.assert_called_once()
    # structlog.info is called with keyword arguments
    call_kwargs = mock_info.call_args.kwargs
    assert call_kwargs["action"] == Action.SEARCH_MOVIE.value
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.RADARR.value
    assert call_kwargs["run_id"] == "test-run-123"
    assert call_kwargs["movie_id"] == "42"
    assert call_kwargs["movie_name"] == "Test Movie"

  def test_log_movie_action_includes_correlation_fields(self) -> None:
    """Test log_movie_action includes movie_id and all correlation fields."""
    mock_info = Mock()
    logger = Mock(spec=structlog.BoundLogger)
    logger.info = mock_info

    movie_id = MovieId(movie_id=123, movie_name="Test Movie")
    log_movie_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    mock_info.assert_called_once()
    call_kwargs = mock_info.call_args.kwargs
    assert call_kwargs["action"] == Action.SEARCH_MOVIE.value
    assert call_kwargs["movie_id"] == "123"
    assert call_kwargs["movie_name"] == "Test Movie"
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.RADARR.value
    assert call_kwargs["run_id"] == "test-run-123"

  def test_log_movie_action_without_name(self) -> None:
    """Test log_movie_action works without movie_name."""
    mock_info = Mock()
    logger = Mock(spec=structlog.BoundLogger)
    logger.info = mock_info

    movie_id = MovieId(movie_id=123, movie_name=None)
    log_movie_action(
      logger=logger,
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    mock_info.assert_called_once()
    call_kwargs = mock_info.call_args.kwargs
    assert call_kwargs["movie_id"] == "123"
    assert call_kwargs["movie_name"] == "None"

  def test_log_series_action_includes_correlation_fields(self) -> None:
    """Test log_series_action includes series_id and all correlation fields."""
    from app.scheduler import SeriesId

    mock_info = Mock()
    logger = Mock(spec=structlog.BoundLogger)
    logger.info = mock_info

    series_id = SeriesId(series_id=456, series_name="Test Series")
    log_series_action(
      logger=logger,
      action=Action.SEARCH_SERIES,
      series_id=series_id,
      target_name="test-target",
      target_type=ArrType.SONARR.value,
      run_id="test-run-123",
    )

    mock_info.assert_called_once()
    call_kwargs = mock_info.call_args.kwargs
    assert call_kwargs["action"] == Action.SEARCH_SERIES.value
    assert call_kwargs["series_id"] == "456"
    assert call_kwargs["series_name"] == "Test Series"
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.SONARR.value
    assert call_kwargs["run_id"] == "test-run-123"

  def test_log_series_action_without_name(self) -> None:
    """Test log_series_action works without series_name."""
    from app.scheduler import SeriesId

    mock_info = Mock()
    logger = Mock(spec=structlog.BoundLogger)
    logger.info = mock_info

    series_id = SeriesId(series_id=456, series_name=None)
    log_series_action(
      logger=logger,
      action=Action.SEARCH_SERIES,
      series_id=series_id,
      target_name="test-target",
      target_type=ArrType.SONARR.value,
      run_id="test-run-123",
    )

    mock_info.assert_called_once()
    call_kwargs = mock_info.call_args.kwargs
    assert call_kwargs["series_id"] == "456"
    assert call_kwargs["series_name"] == "None"
