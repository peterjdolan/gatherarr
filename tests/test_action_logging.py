"""Tests for logging module."""

from typing import Any

from app.action_logging import Action, log_item_action, log_movie_action, log_season_action
from app.config import ArrType
from app.handlers import MovieId, SeasonId


class FakeLogger:
  """Simple fake logger that captures info payloads."""

  def __init__(self) -> None:
    self.entries: list[dict[str, Any]] = []

  def info(self, event: str, **kwargs: Any) -> None:
    self.entries.append({"event": event, **kwargs})


class TestLogging:
  def test_log_item_action(self) -> None:
    """Test log_item_action logs with all provided fields at INFO level."""
    logger = FakeLogger()
    movie_id = MovieId(movie_id=42, movie_name="Test Movie")

    log_item_action(
      logger=logger,  # type: ignore[arg-type]
      action=Action.SEARCH_MOVIE,
      item_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    assert len(logger.entries) == 1
    call_kwargs = logger.entries[0]
    assert call_kwargs["action"] == Action.SEARCH_MOVIE.value
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.RADARR.value
    assert call_kwargs["run_id"] == "test-run-123"
    assert call_kwargs["movie_id"] == "42"
    assert call_kwargs["movie_name"] == "Test Movie"

  def test_log_movie_action_includes_correlation_fields(self) -> None:
    """Test log_movie_action includes movie_id and all correlation fields."""
    logger = FakeLogger()
    movie_id = MovieId(movie_id=123, movie_name="Test Movie")

    log_movie_action(
      logger=logger,  # type: ignore[arg-type]
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    assert len(logger.entries) == 1
    call_kwargs = logger.entries[0]
    assert call_kwargs["action"] == Action.SEARCH_MOVIE.value
    assert call_kwargs["movie_id"] == "123"
    assert call_kwargs["movie_name"] == "Test Movie"
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.RADARR.value
    assert call_kwargs["run_id"] == "test-run-123"

  def test_log_movie_action_without_name(self) -> None:
    """Test log_movie_action works without movie_name."""
    logger = FakeLogger()
    movie_id = MovieId(movie_id=123, movie_name=None)

    log_movie_action(
      logger=logger,  # type: ignore[arg-type]
      action=Action.SEARCH_MOVIE,
      movie_id=movie_id,
      target_name="test-target",
      target_type=ArrType.RADARR.value,
      run_id="test-run-123",
    )

    assert len(logger.entries) == 1
    call_kwargs = logger.entries[0]
    assert call_kwargs["movie_id"] == "123"
    assert call_kwargs["movie_name"] == "None"

  def test_log_season_action_includes_correlation_fields(self) -> None:
    """Test log_season_action includes season correlation fields."""
    logger = FakeLogger()
    season_id = SeasonId(series_id=456, season_number=3, series_name="Test Series")

    log_season_action(
      logger=logger,  # type: ignore[arg-type]
      action=Action.SEARCH_SEASON,
      season_id=season_id,
      target_name="test-target",
      target_type=ArrType.SONARR.value,
      run_id="test-run-123",
    )

    assert len(logger.entries) == 1
    call_kwargs = logger.entries[0]
    assert call_kwargs["action"] == Action.SEARCH_SEASON.value
    assert call_kwargs["series_id"] == "456"
    assert call_kwargs["season_number"] == "3"
    assert call_kwargs["series_name"] == "Test Series"
    assert call_kwargs["target_name"] == "test-target"
    assert call_kwargs["target_type"] == ArrType.SONARR.value
    assert call_kwargs["run_id"] == "test-run-123"

  def test_log_season_action_without_name(self) -> None:
    """Test log_season_action works without series_name."""
    logger = FakeLogger()
    season_id = SeasonId(series_id=456, season_number=5, series_name=None)

    log_season_action(
      logger=logger,  # type: ignore[arg-type]
      action=Action.SEARCH_SEASON,
      season_id=season_id,
      target_name="test-target",
      target_type=ArrType.SONARR.value,
      run_id="test-run-123",
    )

    assert len(logger.entries) == 1
    call_kwargs = logger.entries[0]
    assert call_kwargs["series_id"] == "456"
    assert call_kwargs["season_number"] == "5"
    assert call_kwargs["series_name"] == "None"
