"""Tests for scheduler module."""

import time
from typing import TYPE_CHECKING, Any

import pytest

from app.config import ArrTarget, ArrType
from app.scheduler import Scheduler
from app.state import InMemoryStateStorage, ItemState, RunStatus, StateManager

if TYPE_CHECKING:
  pass


class FakeArrClient:
  """Fake ArrClient for testing."""

  def __init__(self, target: ArrTarget) -> None:
    self.target = target
    self.get_movies_called = False
    self.get_series_called = False
    self.search_movie_called = False
    self.search_series_called = False
    self.search_movie_calls = 0
    self.search_series_calls = 0
    self.search_movie_id: Any | None = None
    self.search_series_id: int | None = None

  async def get_movies(self, logging_ids: dict[str, Any]) -> list[dict]:
    self.get_movies_called = True
    return [
      {"id": 1, "title": "Movie 1", "monitored": True, "hasFile": False},
      {"id": 2, "title": "Movie 2", "monitored": True, "movieFile": {"qualityCutoffNotMet": True}},
    ]

  async def get_series(self, logging_ids: dict[str, Any]) -> list[dict]:
    self.get_series_called = True
    return [
      {"id": 1, "title": "Series 1", "monitored": True, "statistics": {"qualityCutoffNotMet": True}}
    ]

  async def search_movie(self, movie_id: Any, logging_ids: dict[str, Any]) -> dict:
    self.search_movie_called = True
    self.search_movie_calls += 1
    self.search_movie_id = movie_id
    return {"id": 1}

  async def search_series(self, series_id: Any, logging_ids: dict[str, Any]) -> dict:
    self.search_series_called = True
    self.search_series_calls += 1
    self.search_series_id = series_id.series_id if hasattr(series_id, "series_id") else series_id
    return {"id": 1}


class FakeClientWithError:
  """Fake client that raises errors."""

  def __init__(self, target: ArrTarget) -> None:
    self.target = target

  async def get_movies(self, logging_ids: dict[str, Any]) -> list[dict]:
    raise RuntimeError("API error")

  async def get_series(self, logging_ids: dict[str, Any]) -> list[dict]:
    raise RuntimeError("API error")


class FakeClientWithIneligibleItems(FakeArrClient):
  """Fake client that returns items that should not be searched."""

  async def get_movies(self, logging_ids: dict[str, Any]) -> list[dict]:
    self.get_movies_called = True
    return [{"id": 1, "title": "Movie 1", "monitored": False, "hasFile": False}]

  async def get_series(self, logging_ids: dict[str, Any]) -> list[dict]:
    self.get_series_called = True
    return [
      {
        "id": 1,
        "title": "Series 1",
        "monitored": True,
        "statistics": {"episodeFileCount": 10, "totalEpisodeCount": 10},
      }
    ]


class FakeClientWithSingleEligibleMovie(FakeArrClient):
  """Fake client that returns one eligible movie."""

  async def get_movies(self, logging_ids: dict[str, Any]) -> list[dict]:
    self.get_movies_called = True
    return [{"id": 1, "title": "Movie 1", "monitored": True, "hasFile": False}]


class FakeClientWithSearchError(FakeClientWithSingleEligibleMovie):
  """Fake client that fails on movie search."""

  async def search_movie(self, movie_id: Any, logging_ids: dict[str, Any]) -> dict:
    self.search_movie_called = True
    self.search_movie_calls += 1
    raise RuntimeError("Search error")


@pytest.fixture
def state_manager() -> StateManager:
  """Create a StateManager with in-memory storage."""
  return StateManager(InMemoryStateStorage())


def create_target(
  name: str,
  arr_type: ArrType,
  ops_per_interval: int = 10,
  **overrides: Any,
) -> ArrTarget:
  """Create an ArrTarget with common default values."""
  target_kwargs: dict[str, Any] = {
    "name": name,
    "arr_type": arr_type,
    "base_url": "http://test",
    "api_key": "key",
    "ops_per_interval": ops_per_interval,
    "interval_s": 60,
    "item_revisit_timeout_s": 3600,
  }
  target_kwargs.update(overrides)
  return ArrTarget(**target_kwargs)


def create_scheduler(
  target: ArrTarget,
  state_manager: StateManager,
  fake_client: Any,
) -> Scheduler:
  """Create a Scheduler with the given target, state manager, and client."""
  from app.arr_client import ArrClient

  # Fake clients are compatible with ArrClient interface for testing
  arr_clients: dict[str, ArrClient] = {target.name: fake_client}
  return Scheduler([target], state_manager, arr_clients)


class TestScheduler:
  @pytest.mark.asyncio
  async def test_run_once_radarr(self, state_manager: StateManager) -> None:
    target = create_target("test-radarr", ArrType.RADARR)
    fake_client = FakeArrClient(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_movies_called
    assert fake_client.search_movie_called
    # search_movie_id will be a MovieId object (last one processed)
    assert fake_client.search_movie_id is not None
    assert hasattr(fake_client.search_movie_id, "movie_id")
    target_state = state_manager.get_target_state("test-radarr")
    assert target_state.last_status == RunStatus.SUCCESS
    assert target_state.consecutive_failures == 0

  @pytest.mark.asyncio
  async def test_run_once_sonarr(self, state_manager: StateManager) -> None:
    target = create_target("test-sonarr", ArrType.SONARR)
    fake_client = FakeArrClient(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_series_called
    assert fake_client.search_series_called
    assert fake_client.search_series_id == 1

  @pytest.mark.asyncio
  async def test_run_once_respects_ops_limit(self, state_manager: StateManager) -> None:
    target = create_target("test", ArrType.RADARR, ops_per_interval=2)
    fake_client = FakeArrClient(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    target_state = state_manager.get_target_state("test")
    assert len(target_state.items) == 2

  @pytest.mark.asyncio
  async def test_run_once_respects_revisit_timeout(self, state_manager: StateManager) -> None:
    target = create_target("test", ArrType.RADARR)
    target_state = state_manager.get_target_state("test")
    # Set item 1 to be processed 100 seconds ago (within the 3600s timeout)
    target_state.items["1"] = ItemState(
      item_id="1",
      last_processed_timestamp=time.time() - 100.0,
      last_result="success",
      last_status="success",
    )
    # Set item 2 to be processed 100 seconds ago as well, so both should be skipped
    target_state.items["2"] = ItemState(
      item_id="2",
      last_processed_timestamp=time.time() - 100.0,
      last_result="success",
      last_status="success",
    )

    fake_client = FakeArrClient(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_movies_called
    # Both items are within the revisit timeout, so neither should be searched
    assert not fake_client.search_movie_called

  @pytest.mark.asyncio
  async def test_run_once_handles_error(self, state_manager: StateManager) -> None:
    target = create_target("test", ArrType.RADARR)
    fake_client = FakeClientWithError(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    target_state = state_manager.get_target_state("test")
    assert target_state.last_status == RunStatus.ERROR
    assert target_state.consecutive_failures == 1

  @pytest.mark.asyncio
  async def test_run_once_skips_ineligible_movie(self, state_manager: StateManager) -> None:
    target = create_target("test-radarr", ArrType.RADARR)
    fake_client = FakeClientWithIneligibleItems(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_movies_called
    assert not fake_client.search_movie_called

  @pytest.mark.asyncio
  async def test_run_once_skips_series_when_cutoff_met(self, state_manager: StateManager) -> None:
    target = create_target("test-sonarr", ArrType.SONARR)
    fake_client = FakeClientWithIneligibleItems(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_series_called
    assert not fake_client.search_series_called

  @pytest.mark.asyncio
  async def test_run_once_dry_run_does_not_call_search(self, state_manager: StateManager) -> None:
    target = create_target("test-dry-run", ArrType.RADARR, dry_run=True)
    fake_client = FakeClientWithSingleEligibleMovie(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    assert fake_client.get_movies_called
    assert not fake_client.search_movie_called
    target_state = state_manager.get_target_state("test-dry-run")
    assert target_state.items["1"].last_result == "dry_run_search_eligible"

  @pytest.mark.asyncio
  async def test_run_once_respects_max_searches_per_item_per_day(
    self, state_manager: StateManager
  ) -> None:
    target = create_target(
      "test-daily-limit",
      ArrType.RADARR,
      item_revisit_timeout_s=1,
      max_searches_per_item_per_day=1,
    )
    fake_client = FakeClientWithSingleEligibleMovie(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)

    target_state = state_manager.get_target_state("test-daily-limit")
    target_state.items["1"].last_processed_timestamp = time.time() - 10.0

    await scheduler.run_once(target)

    assert fake_client.search_movie_calls == 1

  @pytest.mark.asyncio
  async def test_run_once_respects_search_backoff_after_error(
    self, state_manager: StateManager
  ) -> None:
    target = create_target(
      "test-backoff",
      ArrType.RADARR,
      item_revisit_timeout_s=1,
      search_backoff_s=3600,
    )
    fake_client = FakeClientWithSearchError(target)
    scheduler = create_scheduler(target, state_manager, fake_client)

    await scheduler.run_once(target)
    await scheduler.run_once(target)

    assert fake_client.search_movie_calls == 1
