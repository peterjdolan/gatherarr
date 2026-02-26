"""Tests for item handlers."""

from datetime import datetime, timedelta, timezone

from app.config import ArrTarget, ArrType, TargetSettings
from app.scheduler import MovieHandler, MovieId, SeriesHandler, SeriesId


def movie_target(
  require_monitored: bool = True,
  require_cutoff_unmet: bool = True,
  released_only: bool = False,
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
      item_revisit_timeout_s=3600,
      require_monitored=require_monitored,
      require_cutoff_unmet=require_cutoff_unmet,
      released_only=released_only,
      include_tags=set(include_tags),
      exclude_tags=set(exclude_tags),
    ),
  )


def series_target(
  require_monitored: bool = True,
  require_cutoff_unmet: bool = True,
  released_only: bool = False,
  include_tags: tuple[str, ...] = (),
  exclude_tags: tuple[str, ...] = (),
  min_missing_episodes: int = 0,
  min_missing_percent: float = 0.0,
) -> ArrTarget:
  """Create a series handler target with optional overrides."""
  return ArrTarget(
    name="series-target",
    arr_type=ArrType.SONARR,
    base_url="http://sonarr:8989",
    api_key="key",
    settings=TargetSettings(
      ops_per_interval=1,
      interval_s=60,
      item_revisit_timeout_s=3600,
      require_monitored=require_monitored,
      require_cutoff_unmet=require_cutoff_unmet,
      released_only=released_only,
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
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_not_monitored(self) -> None:
    """Do not search when movie is not monitored."""
    handler = MovieHandler(movie_target())
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": False,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is False

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

    assert handler.should_search(item) is False

  def test_should_search_when_no_file_present(self) -> None:
    """Treat movies with no file as cutoff unmet."""
    handler = MovieHandler(movie_target())
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "hasFile": False,
    }

    assert handler.should_search(item) is True

  def test_should_search_when_monitoring_not_required(self) -> None:
    """Search unmonitored movies when monitoring is disabled."""
    handler = MovieHandler(movie_target(require_monitored=False))
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": False,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is True

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

    assert handler.should_search(item) is True

  def test_should_not_search_unreleased_when_released_only_enabled(self) -> None:
    """Skip unreleased movies when released_only is enabled."""
    handler = MovieHandler(movie_target(released_only=True))
    future_release = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "digitalRelease": future_release,
    }

    assert handler.should_search(item) is False

  def test_should_search_released_movie_when_released_only_enabled(self) -> None:
    """Allow released movies when released_only is enabled."""
    handler = MovieHandler(movie_target(released_only=True))
    past_release = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "digitalRelease": past_release,
    }

    assert handler.should_search(item) is True

  def test_should_search_respects_tag_filters(self) -> None:
    """Apply include/exclude tag filters for movies."""
    handler = MovieHandler(movie_target(include_tags=("4k",), exclude_tags=("skip",)))
    matching_item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "tags": ["4k", "hdr"],
    }
    excluded_item = {
      "id": 43,
      "title": "Excluded Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
      "tags": ["4k", "skip"],
    }

    assert handler.should_search(matching_item) is True
    assert handler.should_search(excluded_item) is False


class TestSeriesHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns SeriesId when item has id."""
    handler = SeriesHandler(series_target())
    item = {"id": 123, "title": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, SeriesId)
    assert result.series_id == 123

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has no id."""
    handler = SeriesHandler(series_target())
    item = {"title": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with series_id."""
    handler = SeriesHandler(series_target())
    item = {"id": 123, "title": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result["series_id"] == "123"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = SeriesHandler(series_target())
    item = {"title": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_series_id_format_for_state(self) -> None:
    """Test SeriesId.format_for_state returns string representation."""
    series_id = SeriesId(series_id=123, series_name="Test Series")
    assert series_id.format_for_state() == "123"

  def test_should_search_when_monitored_and_cutoff_unmet(self) -> None:
    """Search when monitored and quality cutoff is unmet."""
    handler = SeriesHandler(series_target())
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_not_monitored(self) -> None:
    """Do not search when series is not monitored."""
    handler = SeriesHandler(series_target())
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": False,
      "statistics": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is False

  def test_should_search_with_episode_coverage_fallback(self) -> None:
    """Use episode coverage when qualityCutoffNotMet is unavailable."""
    handler = SeriesHandler(series_target())
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"episodeFileCount": 8, "totalEpisodeCount": 10},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_cutoff_met(self) -> None:
    """Do not search when series appears complete at target quality."""
    handler = SeriesHandler(series_target())
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"episodeFileCount": 10, "totalEpisodeCount": 10},
    }

    assert handler.should_search(item) is False

  def test_should_search_when_cutoff_not_required(self) -> None:
    """Search series when cutoff requirement is disabled."""
    handler = SeriesHandler(series_target(require_cutoff_unmet=False))
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"episodeFileCount": 10, "totalEpisodeCount": 10},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_series_when_unreleased_and_released_only_enabled(self) -> None:
    """Skip unreleased series when released_only is enabled."""
    handler = SeriesHandler(series_target(released_only=True))
    future_air_date = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "firstAired": future_air_date,
      "statistics": {"qualityCutoffNotMet": True, "episodeFileCount": 0},
    }

    assert handler.should_search(item) is False

  def test_should_search_series_with_released_episode_when_released_only_enabled(self) -> None:
    """Allow released series when released_only is enabled."""
    handler = SeriesHandler(series_target(released_only=True))
    past_air_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "firstAired": past_air_date,
      "statistics": {"qualityCutoffNotMet": True, "episodeFileCount": 1},
    }

    assert handler.should_search(item) is True

  def test_should_search_series_respects_tag_filters(self) -> None:
    """Apply include/exclude tag filters for series."""
    handler = SeriesHandler(series_target(include_tags=("anime",), exclude_tags=("paused",)))
    matching_item = {
      "id": 123,
      "title": "Matching Series",
      "monitored": True,
      "statistics": {"qualityCutoffNotMet": True},
      "tags": ["anime"],
    }
    excluded_item = {
      "id": 124,
      "title": "Excluded Series",
      "monitored": True,
      "statistics": {"qualityCutoffNotMet": True},
      "tags": ["anime", "paused"],
    }

    assert handler.should_search(matching_item) is True
    assert handler.should_search(excluded_item) is False

  def test_should_search_series_with_min_missing_episode_threshold(self) -> None:
    """Require minimum missing episodes when configured."""
    handler = SeriesHandler(series_target(min_missing_episodes=3))
    below_threshold_item = {
      "id": 123,
      "title": "Below Threshold",
      "monitored": True,
      "statistics": {"episodeFileCount": 9, "totalEpisodeCount": 10},
    }
    above_threshold_item = {
      "id": 124,
      "title": "Above Threshold",
      "monitored": True,
      "statistics": {"episodeFileCount": 6, "totalEpisodeCount": 10},
    }

    assert handler.should_search(below_threshold_item) is False
    assert handler.should_search(above_threshold_item) is True

  def test_should_search_series_with_min_missing_percent_threshold(self) -> None:
    """Require minimum missing percent when configured."""
    handler = SeriesHandler(series_target(min_missing_percent=25.0))
    below_threshold_item = {
      "id": 123,
      "title": "Below Percent",
      "monitored": True,
      "statistics": {"percentOfEpisodes": 85},
    }
    above_threshold_item = {
      "id": 124,
      "title": "Above Percent",
      "monitored": True,
      "statistics": {"percentOfEpisodes": 60},
    }

    assert handler.should_search(below_threshold_item) is False
    assert handler.should_search(above_threshold_item) is True
