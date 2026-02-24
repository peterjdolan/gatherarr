"""Tests for HTTP client implementation."""

from typing import Any

import httpx
import pytest

from app.http_client import HttpxClient


class FakeClient:
  """Fake httpx client for testing."""

  def __init__(
    self, responses: dict[str, Any] | None = None, status_codes: dict[str, int] | None = None
  ) -> None:
    self.responses = responses or {}
    self.status_codes = status_codes or {}
    self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

  async def get(
    self, url: str, headers: dict[str, str] | None = None, timeout: float | None = None
  ) -> "FakeResponse":
    """Fake GET request."""
    self.calls.append(("GET", url, None))
    status = self.status_codes.get(url, 200)
    data = self.responses.get(url, {})
    return FakeResponse(status, data)

  async def post(
    self,
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
    timeout: float | None = None,
  ) -> "FakeResponse":
    """Fake POST request."""
    self.calls.append(("POST", url, json))
    status = self.status_codes.get(url, 200)
    data = self.responses.get(url, {})
    return FakeResponse(status, data)

  async def aclose(self) -> None:
    """Fake close."""
    pass


class FakeResponse:
  """Fake httpx response for testing."""

  def __init__(self, status_code: int, data: Any) -> None:
    self.status_code = status_code
    self._data = data

  def json(self) -> Any:
    """Return JSON data."""
    return self._data

  def raise_for_status(self) -> None:
    """Raise error for non-2xx status."""
    if self.status_code >= 400:
      request = httpx.Request("GET", "http://test")
      response = httpx.Response(self.status_code, request=request)
      error = httpx.HTTPStatusError(f"HTTP {self.status_code}", request=request, response=response)
      raise error


class TestHttpxClient:
  @pytest.mark.asyncio
  async def test_get_success(self) -> None:
    fake_client = FakeClient(responses={"http://test": {"result": "success"}})
    client = HttpxClient(fake_client)
    result = await client.get("http://test", {"X-Key": "value"}, 30.0)

    assert result == {"result": "success"}
    assert ("GET", "http://test", None) in fake_client.calls

  @pytest.mark.asyncio
  async def test_post_success(self) -> None:
    fake_client = FakeClient(responses={"http://test": {"id": 1}})
    client = HttpxClient(fake_client)
    payload = {"name": "test"}
    result = await client.post("http://test", {"X-Key": "value"}, 30.0, payload)

    assert result == {"id": 1}
    assert any(call[0] == "POST" and call[1] == "http://test" for call in fake_client.calls)

  @pytest.mark.asyncio
  async def test_get_error_raises(self) -> None:
    fake_client = FakeClient(status_codes={"http://test": 500})
    client = HttpxClient(fake_client)

    with pytest.raises(httpx.HTTPStatusError):
      await client.get("http://test", {}, 30.0)
