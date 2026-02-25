"""Tests for item handlers."""

from app.scheduler import MovieHandler, MovieId, SeriesHandler, SeriesId


class TestMovieHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns MovieId when item has id."""
    handler = MovieHandler()
    item = {"id": 42, "title": "Test Movie"}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, MovieId)
    assert result.movie_id == 42

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has no id."""
    handler = MovieHandler()
    item = {"title": "Test Movie"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with movie_id."""
    handler = MovieHandler()
    item = {"id": 42, "title": "Test Movie"}

    result = handler.extract_logging_id(item)

    assert result["movie_id"] == "42"
    assert result["movie_name"] == "Test Movie"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = MovieHandler()
    item = {"title": "Test Movie"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_movie_id_format_for_state(self) -> None:
    """Test MovieId.format_for_state returns string representation."""
    movie_id = MovieId(movie_id=42, movie_name="Test Movie")
    assert movie_id.format_for_state() == "42"

  def test_should_search_when_monitored_and_cutoff_unmet(self) -> None:
    """Search when monitored and quality cutoff is unmet."""
    handler = MovieHandler()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_not_monitored(self) -> None:
    """Do not search when movie is not monitored."""
    handler = MovieHandler()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": False,
      "movieFile": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is False

  def test_should_not_search_when_cutoff_met(self) -> None:
    """Do not search when quality cutoff is already met."""
    handler = MovieHandler()
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
    handler = MovieHandler()
    item = {
      "id": 42,
      "title": "Test Movie",
      "monitored": True,
      "hasFile": False,
    }

    assert handler.should_search(item) is True


class TestSeriesHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns SeriesId when item has id."""
    handler = SeriesHandler()
    item = {"id": 123, "title": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, SeriesId)
    assert result.series_id == 123

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has no id."""
    handler = SeriesHandler()
    item = {"title": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with series_id."""
    handler = SeriesHandler()
    item = {"id": 123, "title": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result["series_id"] == "123"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = SeriesHandler()
    item = {"title": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_series_id_format_for_state(self) -> None:
    """Test SeriesId.format_for_state returns string representation."""
    series_id = SeriesId(series_id=123, series_name="Test Series")
    assert series_id.format_for_state() == "123"

  def test_should_search_when_monitored_and_cutoff_unmet(self) -> None:
    """Search when monitored and quality cutoff is unmet."""
    handler = SeriesHandler()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_not_monitored(self) -> None:
    """Do not search when series is not monitored."""
    handler = SeriesHandler()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": False,
      "statistics": {"qualityCutoffNotMet": True},
    }

    assert handler.should_search(item) is False

  def test_should_search_with_episode_coverage_fallback(self) -> None:
    """Use episode coverage when qualityCutoffNotMet is unavailable."""
    handler = SeriesHandler()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"episodeFileCount": 8, "totalEpisodeCount": 10},
    }

    assert handler.should_search(item) is True

  def test_should_not_search_when_cutoff_met(self) -> None:
    """Do not search when series appears complete at target quality."""
    handler = SeriesHandler()
    item = {
      "id": 123,
      "title": "Test Series",
      "monitored": True,
      "statistics": {"episodeFileCount": 10, "totalEpisodeCount": 10},
    }

    assert handler.should_search(item) is False
