"""Tests for item handlers."""

from app.scheduler import MovieHandler, MovieId, SeasonHandler, SeasonId


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


class TestSeasonHandler:
  def test_extract_item_id_with_id(self) -> None:
    """Test extract_item_id returns SeasonId when item has required fields."""
    handler = SeasonHandler()
    item = {"seriesId": 123, "seriesTitle": "Test Series", "seasonNumber": 2}

    result = handler.extract_item_id(item)

    assert result is not None
    assert isinstance(result, SeasonId)
    assert result.series_id == 123
    assert result.season_number == 2

  def test_extract_item_id_without_id(self) -> None:
    """Test extract_item_id returns None when item has missing fields."""
    handler = SeasonHandler()
    item = {"seriesTitle": "Test Series"}

    result = handler.extract_item_id(item)

    assert result is None

  def test_extract_logging_id_with_id(self) -> None:
    """Test extract_logging_id returns dict with season correlation fields."""
    handler = SeasonHandler()
    item = {"seriesId": 123, "seriesTitle": "Test Series", "seasonNumber": 2}

    result = handler.extract_logging_id(item)

    assert result["series_id"] == "123"
    assert result["season_number"] == "2"
    assert result["series_name"] == "Test Series"

  def test_extract_logging_id_without_id(self) -> None:
    """Test extract_logging_id handles missing id."""
    handler = SeasonHandler()
    item = {"seriesTitle": "Test Series"}

    result = handler.extract_logging_id(item)

    assert result == {}

  def test_season_id_format_for_state(self) -> None:
    """Test SeasonId.format_for_state returns composite series/season key."""
    season_id = SeasonId(series_id=123, season_number=4, series_name="Test Series")
    assert season_id.format_for_state() == "123:4"
