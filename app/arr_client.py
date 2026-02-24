"""HTTP client for *arr APIs with retry logic."""

from typing import Any, Protocol, cast

import httpx
import structlog
from tenacity import (
  retry,
  retry_if_exception,
  retry_if_exception_type,
  stop_after_attempt,
  wait_exponential,
)

from app.config import ArrTarget, ArrType

logger = structlog.get_logger()


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
    status_code: int = exception.response.status_code
    return status_code >= 500 or status_code == 429
  return False


class ArrClient:
  """Client for interacting with *arr APIs."""

  def __init__(
    self,
    target: ArrTarget,
    http_client: HttpClient,
    max_retries: int = 3,
    retry_delay_s: float = 1.0,
    timeout_s: float = 30.0,
  ) -> None:
    self.target = target
    self.base_url = target.base_url.rstrip("/")
    self.logging_ids = {
      "target_name": target.name,
      "target_type": target.arr_type.value,
    }
    self.http_client = http_client
    self.max_retries = max_retries
    self.retry_delay_s = retry_delay_s
    self.timeout_s = timeout_s

  def _get_headers(self) -> dict[str, str]:
    """Get HTTP headers for API requests."""
    return {"X-Api-Key": self.target.api_key, "Content-Type": "application/json"}

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
    logger.debug(
      "Making HTTP request",
      method=method,
      url=url,
      has_payload=payload is not None,
      timeout_s=self.timeout_s,
      max_retries=self.max_retries,
      **self.logging_ids,
    )
    retry_decorator = self._make_retry_decorator()

    @retry_decorator
    async def _do_request() -> Any:
      headers = self._get_headers()
      logger.debug(
        "Executing HTTP request",
        method=method,
        url=url,
        has_payload=payload is not None,
        **self.logging_ids,
      )
      if method == "GET":
        result = await self.http_client.get(url, headers, self.timeout_s)
      else:
        result = await self.http_client.post(url, headers, self.timeout_s, payload)
      logger.debug(
        "HTTP request completed",
        method=method,
        url=url,
        has_result=result is not None,
        **self.logging_ids,
      )
      return result

    try:
      return await _do_request()
    except Exception as e:
      logger.debug(
        "HTTP request failed",
        method=method,
        url=url,
        error=str(e)[:200],
        **self.logging_ids,
      )
      raise

  async def get_movies(self) -> list[dict[str, Any]]:
    """Get all movies from Radarr."""
    if self.target.arr_type != ArrType.RADARR:
      raise ValueError(f"get_movies() only supported for radarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/movie"
    logger.debug(
      "Fetching movies",
      action="get_movies",
      url=url,
      **self.logging_ids,
    )
    try:
      result = await self._request("GET", url)
      movie_count = len(result) if isinstance(result, list) else 0
      logger.debug(
        "Fetched movies",
        action="get_movies",
        movie_count=movie_count,
        **self.logging_ids,
      )
      return cast(list[dict[str, Any]], result)
    except Exception as e:
      error_msg = str(e)[:200]
      logger.error(
        "Failed to fetch movies",
        action="get_movies",
        url=url,
        error=error_msg,
        **self.logging_ids,
      )
      raise

  async def get_series(self) -> list[dict[str, Any]]:
    """Get all series from Sonarr."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"get_series() only supported for sonarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/series"
    logger.debug(
      "Fetching series",
      action="get_series",
      url=url,
      **self.logging_ids,
    )
    try:
      result = await self._request("GET", url)
      series_count = len(result) if isinstance(result, list) else 0
      logger.debug(
        "Fetched series",
        action="get_series",
        series_count=series_count,
        **self.logging_ids,
      )
      return cast(list[dict[str, Any]], result)
    except Exception as e:
      error_msg = str(e)[:200]
      logger.error(
        "Failed to fetch series",
        action="get_series",
        url=url,
        error=error_msg,
        **self.logging_ids,
      )
      raise

  async def search_movie(self, movie_id: int) -> dict[str, Any]:
    """Trigger search for a movie in Radarr."""
    if self.target.arr_type != ArrType.RADARR:
      raise ValueError(f"search_movie() only supported for radarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "MoviesSearch", "movieIds": [movie_id]}
    logger.debug(
      "Searching movie",
      movie_id=movie_id,
      action="search_movie",
      url=url,
      payload=payload,
      **self.logging_ids,
    )
    try:
      result = await self._request("POST", url, payload)
      logger.debug(
        "Movie searched",
        movie_id=movie_id,
        action="search_movie",
        result_id=result.get("id") if isinstance(result, dict) else None,
        **self.logging_ids,
      )
      return cast(dict[str, Any], result)
    except Exception as e:
      error_msg = str(e)[:200]
      logger.error(
        "Failed to search movie",
        movie_id=movie_id,
        action="search_movie",
        url=url,
        payload=payload,
        error=error_msg,
        **self.logging_ids,
      )
      raise

  async def search_series(self, series_id: int) -> dict[str, Any]:
    """Trigger search for a series in Sonarr."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"search_series() only supported for sonarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "SeriesSearch", "seriesId": series_id}
    logger.debug(
      "Searching series",
      series_id=series_id,
      action="search_series",
      url=url,
      payload=payload,
      **self.logging_ids,
    )
    try:
      result = await self._request("POST", url, payload)
      logger.debug(
        "Series searched",
        series_id=series_id,
        action="search_series",
        result_id=result.get("id") if isinstance(result, dict) else None,
        **self.logging_ids,
      )
      return cast(dict[str, Any], result)
    except Exception as e:
      error_msg = str(e)[:200]
      logger.error(
        "Failed to search series",
        series_id=series_id,
        action="search_series",
        url=url,
        payload=payload,
        error=error_msg,
        **self.logging_ids,
      )
      raise
