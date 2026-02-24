"""Tests for *arr client module."""

import asyncio
from typing import Any

import httpx
import pytest

from app.arr_client import ArrClient, HttpClient


class FakeHttpClient(HttpClient):
  """Fake HTTP client for testing."""

  def __init__(
    self, responses: dict[str, Any] | None = None, errors: dict[str, BaseException] | None = None
  ) -> None:
    self.responses = responses or {}
    self.errors = errors or {}
    self.calls: list[tuple[str, str]] = []

  async def get(self, url: str, headers: dict[str, str], timeout: float) -> Any:
    """Fake GET request."""
    self.calls.append(("GET", url))
    if url in self.errors:
      raise self.errors[url]
    return self.responses.get(url, [])

  async def post(
    self, url: str, headers: dict[str, str], timeout: float, payload: dict[str, Any] | None = None
  ) -> Any:
    """Fake POST request."""
    self.calls.append(("POST", url))
    if url in self.errors:
      raise self.errors[url]
    return self.responses.get(url, {})


class TestArrClient:
  def test_get_movies_radarr(self) -> None:
    fake_client = FakeHttpClient(
      responses={"http://test/api/v3/movie": [{"id": 1, "title": "Test"}]}
    )
    client = ArrClient("http://test", "key", "radarr", fake_client)

    result = asyncio.run(client.get_movies())
    assert result == [{"id": 1, "title": "Test"}]
    assert ("GET", "http://test/api/v3/movie") in fake_client.calls

  def test_get_movies_wrong_type(self) -> None:
    fake_client = FakeHttpClient()
    client = ArrClient("http://test", "key", "sonarr", fake_client)

    with pytest.raises(ValueError, match="get_movies.*only supported for radarr"):
      asyncio.run(client.get_movies())

  def test_get_series_sonarr(self) -> None:
    fake_client = FakeHttpClient(
      responses={"http://test/api/v3/series": [{"id": 1, "title": "Test"}]}
    )
    client = ArrClient("http://test", "key", "sonarr", fake_client)

    result = asyncio.run(client.get_series())
    assert result == [{"id": 1, "title": "Test"}]

  def test_search_movie(self) -> None:
    fake_client = FakeHttpClient(responses={"http://test/api/v3/command": {"id": 1}})
    client = ArrClient("http://test", "key", "radarr", fake_client)

    result = asyncio.run(client.search_movie(123))
    assert result == {"id": 1}
    assert ("POST", "http://test/api/v3/command") in fake_client.calls

  def test_search_series(self) -> None:
    fake_client = FakeHttpClient(responses={"http://test/api/v3/command": {"id": 1}})
    client = ArrClient("http://test", "key", "sonarr", fake_client)

    result = asyncio.run(client.search_series(456))
    assert result == {"id": 1}

  def test_base_url_stripping(self) -> None:
    fake_client = FakeHttpClient()
    client = ArrClient("http://test/", "key", "radarr", fake_client)

    asyncio.run(client.get_movies())
    assert ("GET", "http://test/api/v3/movie") in fake_client.calls

  def test_get_headers(self) -> None:
    fake_client = FakeHttpClient()
    client = ArrClient("http://test", "test-key", "radarr", fake_client)
    headers = client._get_headers()
    assert headers["X-Api-Key"] == "test-key"
    assert headers["Content-Type"] == "application/json"

  def test_retry_on_retryable_error(self) -> None:
    errors = {
      "http://test/api/v3/movie": httpx.RequestError("Network error"),
    }
    fake_client = FakeHttpClient(errors=errors)
    client = ArrClient("http://test", "key", "radarr", fake_client, max_retries=2)

    with pytest.raises(httpx.RequestError):
      asyncio.run(client.get_movies())

    assert len([c for c in fake_client.calls if c[0] == "GET"]) == 2

  def test_no_retry_on_non_retryable_error(self) -> None:
    request = httpx.Request("GET", "http://test/api/v3/movie")
    response = httpx.Response(404, request=request)
    errors = {
      "http://test/api/v3/movie": httpx.HTTPStatusError(
        "Not found", request=request, response=response
      ),
    }
    fake_client = FakeHttpClient(errors=errors)
    client = ArrClient("http://test", "key", "radarr", fake_client, max_retries=3)

    with pytest.raises(httpx.HTTPStatusError):
      asyncio.run(client.get_movies())

    assert len([c for c in fake_client.calls if c[0] == "GET"]) == 1
