"""HTTP client implementation using httpx."""

from typing import Any, Protocol

import httpx
import structlog

from app.arr_client import HttpClient

logger = structlog.get_logger()


class AsyncHttpClient(Protocol):
  """Protocol for async HTTP client interface."""

  async def get(self, url: str, *args: Any, **kwargs: Any) -> "HttpResponse":
    """Make GET request."""
    ...

  async def post(self, url: str, *args: Any, **kwargs: Any) -> "HttpResponse":
    """Make POST request."""
    ...


class HttpResponse(Protocol):
  """Protocol for HTTP response interface."""

  status_code: int

  def raise_for_status(self) -> None:
    """Raise error for non-2xx status."""
    ...

  def json(self) -> Any:
    """Return JSON data."""
    ...


class HttpxClient(HttpClient):
  """httpx-based HTTP client implementation."""

  def __init__(self, client: AsyncHttpClient | httpx.AsyncClient) -> None:
    self.client = client

  async def get(self, url: str, headers: dict[str, str], timeout: float) -> Any:
    """Make GET request."""
    logger.debug("Executing GET request", url=url, timeout=timeout, has_headers=bool(headers))
    response = await self.client.get(url, headers=headers, timeout=timeout)
    logger.debug("GET request completed", url=url, status_code=response.status_code)
    response.raise_for_status()
    result = response.json()
    logger.debug("GET request response parsed", url=url, has_result=result is not None)
    return result

  async def post(
    self, url: str, headers: dict[str, str], timeout: float, payload: dict[str, Any] | None = None
  ) -> Any:
    """Make POST request."""
    logger.debug(
      "Executing POST request",
      url=url,
      timeout=timeout,
      has_headers=bool(headers),
      has_payload=payload is not None,
    )
    response = await self.client.post(url, headers=headers, json=payload, timeout=timeout)
    logger.debug("POST request completed", url=url, status_code=response.status_code)
    response.raise_for_status()
    result = response.json()
    logger.debug("POST request response parsed", url=url, has_result=result is not None)
    return result
