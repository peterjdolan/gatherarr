"""Tests for item handlers."""

from datetime import datetime, timedelta, timezone

from app.config import ArrTarget, ArrType, TargetSettings
from app.handlers import MovieHandler, MovieId, SeasonHandler, SeasonId


def movie_target(
  require_monitored: bool = True,
  require_cutoff_unmet: bool = True,
  require_released: bool = True,
  include_tags: tuple[str, ...] = (),
  exclude_tags: tuple[str, ...] = (),
) -> ArrTarget:
  """Create a movie handler target with optional overrides."""
  return ArrTarget(
    name="movie-target",
    arr_type=ArrType.RADARR,
    base_url="http://radarr:7878",
    api_key="key",
    settings=TargetSettings(
      ops_per_interval=1,
      interval_s=60,
      item_revisit_s=3600,
      require_monitored=require_monitored,
      require_cutoff_unmet=require_cutoff_unmet,
      require_released=require_released,
      include_tags=set(include_tags),
      exclude_tags=set(exclude_tags),
    ),
  )


def season_target(
  require_monitored: bool = True,
  require_cutoff_unmet: bool = True,
  require_released: bool = True,
  include_tags: tuple[str, ...] = (),
  exclude_tags: tuple[str, ...] = (),
  min_missing_episodes: int = 0,
  min_missing_percent: float = 0.0,
) -> ArrTarget:
  """Create a season handler target with optional overrides."""
  return ArrTarget(
    name="season-target",
    arr_type=ArrType.SONARR,
    base_url="http://sonarr:8989",
    api_key="key",
    settings=TargetSettings(
      ops_per_interval=1,
      interval_s=60,
      item_revisit_s=3600,
      require_monitored=require_monitored,
      require_cutoff_unmet=require_cutoff_unmet,
      require_released=require_released,
      include_tags=set(include_tags),
      exclude_tags=set(exclude_tags),
      min_missing_episodes=min_missing_episodes,
      min_missing_percent=min_missing_percent,
    ),
  )


class TestMovieHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns MovieId when item has id."""
    handler = MovieHandler(movie_target())
    item = {"id": 42, "title": "Test Movie"}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, MovieId)
    assert result.movie_id == 42

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has no id."""
    handler = MovieHandler(movie_target())
    item = {"title": "Test Movie"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with movie_id."""
    handler = MovieHandler(movie_target())
    item = {"id": 42, "title": "Test Movie"}

    result = handler.extract_logging_id(item)

    assert result["movie_id"] == "42"
    assert result["movie_name"] == "Test Movie"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = MovieHandler(movie_target())
    item = {"title": "Test Movie"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_movie_id_format_for_state(self) -> None:
    """Test MovieId.format_for_state returns string representation."""
    movie_id = MovieId(movie_id=42, movie_name="Test Movie")
    assert movie_id.format_for_state() == "42"

  def test_should_search_when_monitored_and_cutoff_unmet(self) -> None:
    """Search when monitored and quality cutoff is unmet."""
    handler = MovieHandler(movie_target())
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "hasFile": True,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item, {}) is True

  def test_should_not_search_when_not_monitored(self) -> None:
    """Do not search when movie is not monitored."""
    handler = MovieHandler(movie_target())
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": False,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item, {}) is False

  def test_should_not_search_when_cutoff_met(self) -> None:
    """Do not search when quality cutoff is already met."""
    handler = MovieHandler(movie_target())
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": False},
      "hasFile": True,
    }

    assert handler.should_search(item, {}) is False

  def test_should_search_when_no_file_present(self) -> None:
    """Treat movies with no file as cutoff unmet."""
    handler = MovieHandler(movie_target())
    past_release = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "hasFile": False,
      "digitalRelease": past_release,
    }

    assert handler.should_search(item, {}) is True

  def test_should_search_when_monitoring_not_required(self) -> None:
    """Search unmonitored movies when monitoring is disabled."""
    handler = MovieHandler(movie_target(require_monitored=False))
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": False,
      "hasFile": True,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item, {}) is True

  def test_should_search_when_cutoff_not_required(self) -> None:
    """Search movies when cutoff requirement is disabled."""
    handler = MovieHandler(movie_target(require_cutoff_unmet=False))
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": False},
      "hasFile": True,
    }

    assert handler.should_search(item, {}) is True

  def test_should_not_search_unreleased_when_require_released_enabled(self) -> None:
    """Skip unreleased movies when require_released is enabled."""
    handler = MovieHandler(movie_target(require_released=True))
    future_release = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "digitalRelease": future_release,
    }

    assert handler.should_search(item, {}) is False

  def test_should_search_released_movie_when_require_released_enabled(self) -> None:
    """Allow released movies when require_released is enabled."""
    handler = MovieHandler(movie_target(require_released=True))
    past_release = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "digitalRelease": past_release,
    }

    assert handler.should_search(item, {}) is True

  def test_should_search_respects_tag_filters(self) -> None:
    """Apply include/exclude tag filters for movies."""
    handler = MovieHandler(movie_target(include_tags=("4k",), exclude_tags=("skip",)))
    matching_item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "hasFile": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "tags": ["4k", "hdr"],
    }
    excluded_item = {
      "id": 43,
      "title": "Excluded Movie",
      "monitored": True,
      "hasFile": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "tags": ["4k", "skip"],
    }

    assert handler.should_search(matching_item, {}) is True
    assert handler.should_search(excluded_item, {}) is False


class TestSeasonHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns SeasonId when item has required fields."""
    handler = SeasonHandler(season_target())
    item = {"seriesId": 123, "seriesTitle": "Test Series", "seasonNumber": 2}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, SeasonId)
    assert result.series_id == 123
    assert result.season_number == 2

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has missing fields."""
    handler = SeasonHandler(season_target())
    item = {"seriesTitle": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with season correlation fields."""
    handler = SeasonHandler(season_target())
    item = {"seriesId": 123, "seriesTitle": "Test Series", "seasonNumber": 2}

    result = handler.extract_logging_id(item)

    assert result["series_id"] == "123"
    assert result["season_number"] == "2"
    assert result["series_name"] == "Test Series"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = SeasonHandler(season_target())
    item = {"seriesTitle": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_season_id_format_for_state(self) -> None:
    """Test SeasonId.format_for_state returns composite series/season key."""
    season_id = SeasonId(series_id=123, season_number=4, series_name="Test Series")
    assert season_id.format_for_state() == "123:4"
