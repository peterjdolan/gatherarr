"""HTTP client for *arr APIs with retry logic."""

from typing import Any, Protocol

import httpx
from tenacity import (
  retry,
  retry_if_exception,
  retry_if_exception_type,
  stop_after_attempt,
  wait_exponential,
)


class HttpClient(Protocol):
  """Protocol for HTTP client operations."""

  async def get(self, url: str, headers: dict[str, str], timeout: float) -> Any:
    """Make GET request."""
    ...

  async def post(
    self, url: str, headers: dict[str, str], timeout: float, payload: dict[str, Any] | None = None
  ) -> Any:
    """Make POST request."""
    ...


def _is_retryable_response_error(exception: BaseException) -> bool:
  """Check if HTTPStatusError is retryable (5xx or 429)."""
  if isinstance(exception, httpx.HTTPStatusError):
    return exception.response.status_code >= 500 or exception.response.status_code == 429
  return False


class ArrClient:
  """Client for interacting with *arr APIs."""

  def __init__(
    self,
    base_url: str,
    api_key: str,
    arr_type: str,
    http_client: HttpClient,
    max_retries: int = 3,
    retry_delay_s: float = 1.0,
    timeout_s: float = 30.0,
  ) -> None:
    self.base_url = base_url.rstrip("/")
    self.api_key = api_key
    self.arr_type = arr_type
    self.http_client = http_client
    self.max_retries = max_retries
    self.retry_delay_s = retry_delay_s
    self.timeout_s = timeout_s

  def _get_headers(self) -> dict[str, str]:
    """Get HTTP headers for API requests."""
    return {"X-Api-Key": self.api_key, "Content-Type": "application/json"}

  def _make_retry_decorator(self) -> Any:
    """Create a retry decorator with instance-specific configuration."""
    return retry(
      stop=stop_after_attempt(self.max_retries),
      wait=wait_exponential(multiplier=self.retry_delay_s, min=self.retry_delay_s, max=10.0),
      retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException, TimeoutError))
      | retry_if_exception(_is_retryable_response_error),
      reraise=True,
    )

  async def _request(self, method: str, url: str, payload: dict[str, Any] | None = None) -> Any:
    """Make HTTP request with retry logic using tenacity."""
    retry_decorator = self._make_retry_decorator()

    @retry_decorator
    async def _do_request() -> Any:
      headers = self._get_headers()
      if method == "GET":
        result = await self.http_client.get(url, headers, self.timeout_s)
      else:
        result = await self.http_client.post(url, headers, self.timeout_s, payload)
      return result

    return await _do_request()

  async def get_movies(self) -> list[dict[str, Any]]:
    """Get all movies from Radarr."""
    if self.arr_type != "radarr":
      raise ValueError(f"get_movies() only supported for radarr, got {self.arr_type}")
    url = f"{self.base_url}/api/v3/movie"
    return await self._request("GET", url)

  async def get_series(self) -> list[dict[str, Any]]:
    """Get all series from Sonarr."""
    if self.arr_type != "sonarr":
      raise ValueError(f"get_series() only supported for sonarr, got {self.arr_type}")
    url = f"{self.base_url}/api/v3/series"
    return await self._request("GET", url)

  async def search_movie(self, movie_id: int) -> dict[str, Any]:
    """Trigger search for a movie in Radarr."""
    if self.arr_type != "radarr":
      raise ValueError(f"search_movie() only supported for radarr, got {self.arr_type}")
    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "MoviesSearch", "movieIds": [movie_id]}
    return await self._request("POST", url, payload)

  async def search_series(self, series_id: int) -> dict[str, Any]:
    """Trigger search for a series in Sonarr."""
    if self.arr_type != "sonarr":
      raise ValueError(f"search_series() only supported for sonarr, got {self.arr_type}")
    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "SeriesSearch", "seriesId": series_id}
    return await self._request("POST", url, payload)
