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

from app.action_logging import Action
from app.config import ArrTarget, ArrType
from app.metrics import request_errors_total, requests_total

if TYPE_CHECKING:
  from app.handlers import MovieId, SeasonId

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
    *,
    max_retries: int | None = None,
    retry_initial_delay_s: float | None = None,
    retry_backoff_exponent: float | None = None,
    retry_max_delay_s: float | None = None,
    timeout_s: float | None = None,
  ) -> None:
    """Initialize ArrClient. Retry and timeout params from target.settings when None."""
    settings = target.settings
    self.target = target
    self.base_url = target.base_url.rstrip("/")
    self.http_client = http_client
    self.max_retries = max_retries if max_retries is not None else settings.http_max_retries
    self.retry_initial_delay_s = (
      retry_initial_delay_s
      if retry_initial_delay_s is not None
      else settings.http_retry_initial_delay_s
    )
    self.retry_backoff_exponent = (
      retry_backoff_exponent
      if retry_backoff_exponent is not None
      else settings.http_retry_backoff_exponent
    )
    self.retry_max_delay_s = (
      retry_max_delay_s if retry_max_delay_s is not None else settings.http_retry_max_delay_s
    )
    self.timeout_s = timeout_s if timeout_s is not None else settings.http_timeout_s

  def _get_headers(self) -> dict[str, str]:
    """Get HTTP headers for API requests."""
    return {"X-Api-Key": self.target.api_key, "Content-Type": "application/json"}

  def _make_retry_decorator(self) -> Any:
    """Create a retry decorator with instance-specific configuration."""
    return retry(
      stop=stop_after_attempt(self.max_retries + 1),
      wait=wait_exponential(
        multiplier=self.retry_initial_delay_s,
        min=self.retry_initial_delay_s,
        max=self.retry_max_delay_s,
        exp_base=self.retry_backoff_exponent,
      ),
      retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException, TimeoutError))
      | retry_if_exception(_is_retryable_response_error),
      reraise=True,
    )

  async def _request(
    self,
    method: str,
    url: str,
    operation: str,
    logging_ids: dict[str, Any],
    payload: dict[str, Any] | None = None,
  ) -> Any:
    """Make HTTP request with retry logic using tenacity."""
    target_name = self.target.name
    arr_type = self.target.arr_type.value
    requests_total.labels(target=target_name, type=arr_type, operation=operation).inc()

    request_logging_ids = {
      "method": method,
      "url": url,
      "has_payload": payload is not None,
      "timeout_s": self.timeout_s,
      "http_max_retries": self.max_retries,
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
      request_errors_total.labels(target=target_name, type=arr_type, operation=operation).inc()
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
      result = await self._request("GET", url, Action.GET_MOVIES, get_movies_logging_ids)
      movies = cast(list[dict[str, Any]], result)
      logger.debug("Fetched movies", movie_count=len(movies), **get_movies_logging_ids)
      return movies
    except Exception as e:
      logger.exception(
        "Exception while fetching movies",
        exception=e,
        **get_movies_logging_ids,
      )
      raise

  def _extract_seasons_from_series(
    self,
    series_items: list[dict[str, Any]],
    logging_ids: dict[str, Any],
  ) -> list[dict[str, Any]]:
    """Flatten Sonarr series payload into season-level items."""
    seasons: list[dict[str, Any]] = []
    for series in series_items:
      series_id = series.get("id")
      season_entries = series.get("seasons")
      if series_id is None or season_entries is None:
        continue

      series_name = series.get("title")
      series_monitored = series.get("monitored")
      series_tags = series.get("tags")
      series_statistics = series.get("statistics")
      series_first_aired = series.get("firstAired")
      for season in season_entries:
        season_number = season.get("seasonNumber")
        if season_number is None:
          continue

        season_monitored = season.get("monitored")
        season_statistics = season.get("statistics")

        seasons.append(
          {
            "seriesId": series_id,
            "seriesTitle": series_name,
            "seasonNumber": season_number,
            "seriesMonitored": series_monitored,
            "seriesTags": series_tags,
            "seriesStatistics": series_statistics,
            "seriesFirstAired": series_first_aired,
            "seasonMonitored": season_monitored,
            "seasonStatistics": season_statistics,
          }
        )

    logger.debug("Extracted seasons from series payload", season_count=len(seasons), **logging_ids)
    return seasons

  async def get_seasons(self, logging_ids: dict[str, Any]) -> list[dict[str, Any]]:
    """Get season-level search items from Sonarr series payloads."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"get_seasons() only supported for sonarr, got {self.target.arr_type}")
    url = f"{self.base_url}/api/v3/series"

    get_seasons_logging_ids = {
      "action": Action.GET_SEASONS,
      "url": url,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Fetching series for season extraction", **get_seasons_logging_ids)
    try:
      result = await self._request("GET", url, Action.GET_SEASONS, get_seasons_logging_ids)
      series_items = cast(list[dict[str, Any]], result)
      series_count = len(series_items)
      season_items = self._extract_seasons_from_series(series_items, get_seasons_logging_ids)
      logger.debug(
        "Fetched seasons",
        series_count=series_count,
        season_count=len(season_items),
        **get_seasons_logging_ids,
      )
      return season_items
    except Exception as e:
      logger.exception(
        "Exception while fetching seasons",
        exception=e,
        **get_seasons_logging_ids,
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
      result = await self._request("POST", url, Action.SEARCH_MOVIE, search_logging_ids, payload)
      logger.debug("Movie searched", **search_logging_ids)
      return cast(dict[str, Any], result)
    except Exception as e:
      logger.exception(
        "Exception while searching movie",
        exception=e,
        **search_logging_ids,
      )
      raise

  async def search_season(
    self, season_id: "SeasonId", logging_ids: dict[str, Any]
  ) -> dict[str, Any]:
    """Trigger search for a season in Sonarr."""
    if self.target.arr_type != ArrType.SONARR:
      raise ValueError(f"search_season() only supported for sonarr, got {self.target.arr_type}")

    url = f"{self.base_url}/api/v3/command"
    payload = {
      "name": "SeasonSearch",
      "seriesId": season_id.series_id,
      "seasonNumber": season_id.season_number,
    }
    search_logging_ids = {
      "action": Action.SEARCH_SEASON,
      "url": url,
      "payload": payload,
      "series_id": season_id.series_id,
      "season_number": season_id.season_number,
      "series_name": season_id.series_name,
      **logging_ids,
      **self.target.logging_ids(),
    }
    logger.debug("Searching season", **search_logging_ids)
    try:
      result = await self._request("POST", url, Action.SEARCH_SEASON, search_logging_ids, payload)
      logger.debug("Season searched", **search_logging_ids)
      return cast(dict[str, Any], result)
    except Exception as e:
      logger.exception(
        "Exception while searching season",
        exception=e,
        **search_logging_ids,
      )
      raise
