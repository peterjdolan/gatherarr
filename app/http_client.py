"""HTTP client implementation using httpx."""

from typing import Any

import httpx

from app.arr_client import HttpClient


class HttpxClient(HttpClient):
  """httpx-based HTTP client implementation."""

  def __init__(self, client: httpx.AsyncClient) -> None:
    self.client = client

  async def get(self, url: str, headers: dict[str, str], timeout: float) -> Any:
    """Make GET request."""
    response = await self.client.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()

  async def post(
    self, url: str, headers: dict[str, str], timeout: float, payload: dict[str, Any] | None = None
  ) -> Any:
    """Make POST request."""
    response = await self.client.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()
