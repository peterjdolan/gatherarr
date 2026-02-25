"""HTTP client for *arr APIs with retry logic."""

from typing import TYPE_CHECKING, Any, Protocol, cast

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
from app.logging import Action

if TYPE_CHECKING:
  from app.scheduler import MovieId, SeriesId

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

  async def _request(
    self,
    method: str,
    url: str,
    logging_ids: dict[str, Any],
    payload: dict[str, Any] | None = None,
  ) -> Any:
    """Make HTTP request with retry logic using tenacity."""
    request_logging_ids = {
      "method": method,
      "url": url,
      "has_payload": payload is not None,
      "timeout_s": self.timeout_s,
      "max_retries": self.max_retries,
      **self.target.logging_ids(),
      **logging_ids,
    }
    logger.debug("Making HTTP request", **request_logging_ids)
    retry_decorator = self._make_retry_decorator()

    attempt = 0

    @retry_decorator
    async def _do_request() -> Any:
      nonlocal attempt
      attempt += 1

      headers = self._get_headers()
      logger.debug("Executing HTTP request", attempt=attempt, **request_logging_ids)
      if method == "GET":
        result = await self.http_client.get(url, headers, self.timeout_s)
      else:
        result = await self.http_client.post(url, headers, self.timeout_s, payload)
      logger.debug(
        "HTTP request completed",
        attempt=attempt,
        has_result=result is not None,
        **request_logging_ids,
      )
      return result

    try:
      return await _do_request()
    except Exception as e:
      logger.exception(
        "Exception while making HTTP request",
        exception=e,
        total_attempts=attempt + 1,
        **request_logging_ids,
      )
      raise

  async def get_movies(self, logging_ids: dict[str, Any]) -> list[dict[str, Any]]:
    """Get all movies from Radarr."""
    if self.target.arr_type != ArrType.RADARR:
      raise ValueError(f"get_movies() only supported for radarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/movie"
    get_movies_logging_ids = {
      "action": Action.GET_MOVIES,
      "url": url,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Fetching movies", **get_movies_logging_ids)
    try:
      result = await self._request("GET", url, get_movies_logging_ids)
      movie_count = len(result) if isinstance(result, list) else 0
      logger.debug("Fetched movies", movie_count=movie_count, **get_movies_logging_ids)
      return cast(list[dict[str, Any]], result)
    except Exception as e:
      logger.exception(
        "Exception while fetching movies",
        exception=e,
        **get_movies_logging_ids,
      )
      raise

  async def get_series(self, logging_ids: dict[str, Any]) -> list[dict[str, Any]]:
    """Get all series from Sonarr."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"get_series() only supported for sonarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/series"

    get_series_logging_ids = {
      "action": Action.GET_SERIES,
      "url": url,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Fetching series", **get_series_logging_ids)
    try:
      result = await self._request("GET", url, get_series_logging_ids)
      series_count = len(result) if isinstance(result, list) else 0
      logger.debug("Fetched series", series_count=series_count, **get_series_logging_ids)
      return cast(list[dict[str, Any]], result)
    except Exception as e:
      logger.exception(
        "Exception while fetching series",
        exception=e,
        **get_series_logging_ids,
      )
      raise

  async def search_movie(self, movie_id: "MovieId", logging_ids: dict[str, Any]) -> dict[str, Any]:
    """Trigger search for a movie in Radarr."""
    if self.target.arr_type != ArrType.RADARR:
      raise ValueError(f"search_movie() only supported for radarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "MoviesSearch", "movieIds": [movie_id.movie_id]}

    search_logging_ids = {
      "action": Action.SEARCH_MOVIE,
      "url": url,
      "payload": payload,
      "movie_id": movie_id.movie_id,
      "movie_name": movie_id.movie_name,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Searching movie", **search_logging_ids)
    try:
      result = await self._request("POST", url, search_logging_ids, payload)
      logger.debug("Movie searched", **search_logging_ids)
      return cast(dict[str, Any], result)
    except Exception as e:
      logger.exception(
        "Exception while searching movie",
        exception=e,
        **search_logging_ids,
      )
      raise

  async def search_series(
    self, series_id: "SeriesId", logging_ids: dict[str, Any]
  ) -> dict[str, Any]:
    """Trigger search for a series in Sonarr."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"search_series() only supported for sonarr, got {self.target.arr_type}")

    url = f"{self.base_url}/api/v3/command"
    payload = {"name": "SeriesSearch", "seriesId": series_id.series_id}
    search_logging_ids = {
      "action": Action.SEARCH_SERIES,
      "url": url,
      "payload": payload,
      "series_id": series_id.series_id,
      "series_name": series_id.series_name,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Searching series", **search_logging_ids)
    try:
      result = await self._request("POST", url, search_logging_ids, payload)
      logger.debug("Series searched", **search_logging_ids)
      return cast(dict[str, Any], result)
    except Exception as e:
      logger.exception(
        "Exception while searching series",
        exception=e,
        **search_logging_ids,
      )
      raise
