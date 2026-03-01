"""Tests for *arr client module."""

import asyncio
import json
from typing import Any, Mapping

import httpx
import pytest

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType, TargetSettings
from app.handlers import MovieId, SeasonId


def _url_base(url: str) -> str:
  """Strip query string for lookup; generated clients add params like excludeLocalCovers."""
  if "?" in url:
    return url.split("?")[0]
  return url


class FakeAsyncTransport(httpx.AsyncBaseTransport):
  """Fake transport for testing that returns predefined responses."""

  def __init__(
    self,
    responses: dict[str, Any] | None = None,
    errors: Mapping[str, BaseException] | None = None,
  ) -> None:
    self.responses = responses or {}
    self.errors = errors or {}
    self.calls: list[tuple[str, str]] = []
    self.post_payloads: list[dict[str, Any] | None] = []

  async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
    """Handle request and return fake response."""
    url = str(request.url)
    self.calls.append((request.method, url))
    url_key = _url_base(url)

    if url_key in self.errors:
      raise self.errors[url_key]

    if request.method == "POST":
      try:
        body = request.content
        self.post_payloads.append(json.loads(body) if body else None)
      except json.JSONDecodeError, TypeError:
        self.post_payloads.append(None)

    data = self.responses.get(url_key)
    if data is not None:
      return httpx.Response(200, json=data)
    return httpx.Response(200, json=[])


def _make_fake_client(
  responses: dict[str, Any] | None = None,
  errors: Mapping[str, BaseException] | None = None,
  base_url: str = "http://test",
) -> httpx.AsyncClient:
  """Create an httpx.AsyncClient with FakeAsyncTransport."""
  transport = FakeAsyncTransport(responses=responses, errors=errors)
  return httpx.AsyncClient(
    base_url=base_url,
    transport=transport,
    headers={"X-Api-Key": "key", "Content-Type": "application/json"},
  )


def _get_transport(client: httpx.AsyncClient) -> FakeAsyncTransport:
  """Extract the FakeAsyncTransport from the client for assertions."""
  transport = client._transport
  assert isinstance(transport, FakeAsyncTransport)
  return transport


def radarr_target() -> ArrTarget:
  """Create a test Radarr target."""
  return ArrTarget(
    name="test-radarr",
    arr_type=ArrType.RADARR,
    base_url="http://test",
    api_key="key",
    settings=TargetSettings(
      ops_per_interval=10,
      interval_s=60,
      item_revisit_s=3600,
    ),
  )


def sonarr_target() -> ArrTarget:
  """Create a test Sonarr target."""
  return ArrTarget(
    name="test-sonarr",
    arr_type=ArrType.SONARR,
    base_url="http://test",
    api_key="key",
    settings=TargetSettings(
      ops_per_interval=10,
      interval_s=60,
      item_revisit_s=3600,
    ),
  )


class TestArrClient:
  def test_get_movies_radarr(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(responses={"http://test/api/v3/movie": [{"id": 1, "title": "Test"}]})
      target = radarr_target()
      client = ArrClient(target, http_client=fake)
      try:
        result = await client.get_movies({})
        assert result == [{"id": 1, "title": "Test"}]
        transport = _get_transport(fake)
        assert any("api/v3/movie" in c[1] for c in transport.calls if c[0] == "GET")
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_get_movies_wrong_type(self) -> None:
    async def run() -> None:
      fake = _make_fake_client()
      target = sonarr_target()
      client = ArrClient(target, http_client=fake)
      try:
        with pytest.raises(ValueError, match="get_movies.*only supported for radarr"):
          await client.get_movies({})
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_get_seasons_sonarr(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(
        responses={
          "http://test/api/v3/series": [
            {"id": 1, "title": "Test", "seasons": [{"seasonNumber": 1}, {"seasonNumber": 2}]},
            {"id": 2, "title": "Other", "seasons": [{"seasonNumber": 0}]},
          ]
        }
      )
      target = sonarr_target()
      client = ArrClient(target, http_client=fake)
      try:
        result = await client.get_seasons({})
        assert len(result) == 3
        assert result[0]["seriesId"] == 1
        assert result[0]["seriesTitle"] == "Test"
        assert result[0]["seasonNumber"] == 1
        assert result[1]["seriesId"] == 1
        assert result[1]["seriesTitle"] == "Test"
        assert result[1]["seasonNumber"] == 2
        assert result[2]["seriesId"] == 2
        assert result[2]["seriesTitle"] == "Other"
        assert result[2]["seasonNumber"] == 0
        for item in result:
          assert "seriesMonitored" in item
          assert "seriesTags" in item
          assert "seriesStatistics" in item
          assert "seriesFirstAired" in item
          assert "seasonMonitored" in item
          assert "seasonStatistics" in item
        transport = _get_transport(fake)
        assert any("api/v3/series" in c[1] for c in transport.calls if c[0] == "GET")
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_search_movie(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(responses={"http://test/api/v3/command": {"id": 1}})
      target = radarr_target()
      client = ArrClient(target, http_client=fake)
      try:
        movie_id = MovieId(movie_id=123, movie_name="Test Movie")
        result = await client.search_movie(movie_id, {})
        assert result == {"id": 1}
        transport = _get_transport(fake)
        assert ("POST", "http://test/api/v3/command") in transport.calls
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_search_season(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(responses={"http://test/api/v3/command": {"id": 1}})
      target = sonarr_target()
      client = ArrClient(target, http_client=fake)
      try:
        season_id = SeasonId(series_id=456, season_number=3, series_name="Test Series")
        result = await client.search_season(season_id, {})
        assert result == {"id": 1}
        transport = _get_transport(fake)
        assert transport.post_payloads[0] == {
          "name": "SeasonSearch",
          "seriesId": 456,
          "seasonNumber": 3,
        }
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_base_url_stripping(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(
        base_url="http://test",
        responses={"http://test/api/v3/movie": []},
      )
      target = ArrTarget(
        name="test",
        arr_type=ArrType.RADARR,
        base_url="http://test/",
        api_key="key",
        settings=TargetSettings(
          ops_per_interval=10,
          interval_s=60,
          item_revisit_s=3600,
        ),
      )
      client = ArrClient(target, http_client=fake)
      try:
        await client.get_movies({})
        transport = _get_transport(fake)
        assert any("api/v3/movie" in c[1] for c in transport.calls if c[0] == "GET")
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_get_headers(self) -> None:
    fake = _make_fake_client()
    target = ArrTarget(
      name="test",
      arr_type=ArrType.RADARR,
      base_url="http://test",
      api_key="test-key",
      settings=TargetSettings(
        ops_per_interval=10,
        interval_s=60,
        item_revisit_s=3600,
      ),
    )
    client = ArrClient(target, http_client=fake)
    headers = client._get_headers()
    assert headers["X-Api-Key"] == "test-key"
    assert headers["Content-Type"] == "application/json"

  def test_retry_on_retryable_error(self) -> None:
    async def run() -> None:
      fake = _make_fake_client(
        errors={"http://test/api/v3/movie": httpx.RequestError("Network error")}
      )
      target = radarr_target()
      client = ArrClient(target, http_client=fake, max_retries=1)
      try:
        with pytest.raises(httpx.RequestError):
          await client.get_movies({})
        transport = _get_transport(fake)
        assert len([c for c in transport.calls if c[0] == "GET"]) == 2
      finally:
        await client.aclose()

    asyncio.run(run())

  def test_no_retry_on_non_retryable_error(self) -> None:
    async def run() -> None:
      request = httpx.Request("GET", "http://test/api/v3/movie")
      response = httpx.Response(404, request=request)
      fake = _make_fake_client(
        errors={
          "http://test/api/v3/movie": httpx.HTTPStatusError(
            "Not found", request=request, response=response
          ),
        }
      )
      target = radarr_target()
      client = ArrClient(target, http_client=fake, max_retries=3)
      try:
        with pytest.raises(httpx.HTTPStatusError):
          await client.get_movies({})
        transport = _get_transport(fake)
        assert len([c for c in transport.calls if c[0] == "GET"]) == 1
      finally:
        await client.aclose()

    asyncio.run(run())
