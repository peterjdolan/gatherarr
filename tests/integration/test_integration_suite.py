"""Integration tests for Arr interactions, state recovery, and metrics scraping."""

import json
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterator

import httpx
import pytest

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
from app.http_client import HttpxClient
from app.main import create_web_app
from app.scheduler import MovieId, Scheduler, SeriesId
from app.state import FileStateStorage, RunStatus, StateManager

RouteKey = tuple[str, str]


@dataclass(frozen=True)
class ResponseSpec:
  """Response specification for a fake Arr endpoint."""

  status_code: int
  body: Any
  delay_s: float = 0.0


@dataclass(frozen=True)
class CapturedRequest:
  """Request data captured by the fake Arr server."""

  method: str
  path: str
  body_text: str


class FakeArrServer:
  """In-process fake Arr HTTP server for integration testing."""

  def __init__(self, responses: dict[RouteKey, list[ResponseSpec]]) -> None:
    self._responses = {route: list(route_responses) for route, route_responses in responses.items()}
    self._captured_requests: list[CapturedRequest] = []
    self._lock = threading.Lock()
    self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._build_handler())
    self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

  def _build_handler(self) -> type[BaseHTTPRequestHandler]:
    parent = self

    class RequestHandler(BaseHTTPRequestHandler):
      def do_GET(self) -> None:  # noqa: N802
        parent._handle_request(self, "GET")

      def do_POST(self) -> None:  # noqa: N802
        parent._handle_request(self, "POST")

      def log_message(self, format: str, *args: object) -> None:
        # Silence test server logs to keep test output focused on assertions.
        return

    return RequestHandler

  def _handle_request(self, handler: BaseHTTPRequestHandler, method: str) -> None:
    content_length_header = handler.headers.get("Content-Length", "0")
    content_length = int(content_length_header)
    body_text = ""
    if content_length > 0:
      body_text = handler.rfile.read(content_length).decode("utf-8")

    with self._lock:
      self._captured_requests.append(
        CapturedRequest(method=method, path=handler.path, body_text=body_text)
      )
      response = self._select_response(method, handler.path)

    if response.delay_s > 0:
      time.sleep(response.delay_s)

    response_payload = json.dumps(response.body).encode("utf-8")
    handler.send_response(response.status_code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(response_payload)))
    handler.end_headers()
    try:
      handler.wfile.write(response_payload)
    except (BrokenPipeError, ConnectionResetError):
      # Timeouts intentionally close connections from the client side.
      pass

  def _select_response(self, method: str, path: str) -> ResponseSpec:
    key = (method, path)
    if key not in self._responses:
      return ResponseSpec(status_code=404, body={"error": "unconfigured_route"})

    configured_responses = self._responses[key]
    if len(configured_responses) > 1:
      return configured_responses.pop(0)
    return configured_responses[0]

  @property
  def base_url(self) -> str:
    """Base URL for this fake server."""
    host, port = self._server.server_address
    return f"http://{host}:{port}"

  def start(self) -> None:
    """Start the fake server thread."""
    self._thread.start()

  def stop(self) -> None:
    """Stop the fake server thread."""
    self._server.shutdown()
    self._server.server_close()
    self._thread.join(timeout=2.0)

  def request_count(self, method: str, path: str) -> int:
    """Count captured requests for a method/path pair."""
    return len(self.requests_for(method, path))

  def requests_for(self, method: str, path: str) -> list[CapturedRequest]:
    """Get captured requests for a method/path pair."""
    with self._lock:
      return [
        request
        for request in self._captured_requests
        if request.method == method and request.path == path
      ]


@contextmanager
def running_fake_arr_server(
  responses: dict[RouteKey, list[ResponseSpec]],
) -> Iterator[FakeArrServer]:
  """Run a fake Arr server for the duration of the context."""
  server = FakeArrServer(responses)
  server.start()
  try:
    yield server
  finally:
    server.stop()


def create_target(name: str, arr_type: ArrType, base_url: str, ops_per_interval: int) -> ArrTarget:
  """Build a target for integration tests."""
  return ArrTarget(
    name=name,
    arr_type=arr_type,
    base_url=base_url,
    api_key="integration-key",
    ops_per_interval=ops_per_interval,
    interval_s=60,
    item_revisit_timeout_s=3600,
  )


def assert_metric_line(metrics_text: str, metric_name: str, required_fragments: list[str]) -> None:
  """Assert that a metric line contains all required label fragments."""
  metric_lines = [line for line in metrics_text.splitlines() if line.startswith(f"{metric_name}{{")]
  assert metric_lines, f"No metric lines found for {metric_name}"
  matching_lines = [
    line for line in metric_lines if all(fragment in line for fragment in required_fragments)
  ]
  assert matching_lines, f"No {metric_name} line matched fragments: {required_fragments}"


@pytest.mark.asyncio
async def test_radarr_success_flow_with_real_http_stack() -> None:
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=200, body=[{"id": 11, "title": "Integration Movie"}]),
    ],
    ("POST", "/api/v3/command"): [
      ResponseSpec(status_code=200, body={"id": 501, "status": "queued"}),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-radarr-success", ArrType.RADARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )

      movies = await arr_client.get_movies({"run_id": "integration-radarr-success"})
      assert movies == [{"id": 11, "title": "Integration Movie"}]

      command_result = await arr_client.search_movie(
        MovieId(movie_id=11, movie_name="Integration Movie"),
        {"run_id": "integration-radarr-success"},
      )
      assert command_result == {"id": 501, "status": "queued"}

    assert fake_server.request_count("GET", "/api/v3/movie") == 1
    command_requests = fake_server.requests_for("POST", "/api/v3/command")
    assert len(command_requests) == 1
    assert json.loads(command_requests[0].body_text) == {"name": "MoviesSearch", "movieIds": [11]}


@pytest.mark.asyncio
async def test_sonarr_success_flow_with_real_http_stack() -> None:
  responses = {
    ("GET", "/api/v3/series"): [
      ResponseSpec(status_code=200, body=[{"id": 22, "title": "Integration Series"}]),
    ],
    ("POST", "/api/v3/command"): [
      ResponseSpec(status_code=200, body={"id": 601, "status": "queued"}),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-sonarr-success", ArrType.SONARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )

      series = await arr_client.get_series({"run_id": "integration-sonarr-success"})
      assert series == [{"id": 22, "title": "Integration Series"}]

      command_result = await arr_client.search_series(
        SeriesId(series_id=22, series_name="Integration Series"),
        {"run_id": "integration-sonarr-success"},
      )
      assert command_result == {"id": 601, "status": "queued"}

    assert fake_server.request_count("GET", "/api/v3/series") == 1
    command_requests = fake_server.requests_for("POST", "/api/v3/command")
    assert len(command_requests) == 1
    assert json.loads(command_requests[0].body_text) == {"name": "SeriesSearch", "seriesId": 22}


@pytest.mark.asyncio
async def test_non_retryable_4xx_error_does_not_retry() -> None:
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=404, body={"message": "not_found"}),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-4xx", ArrType.RADARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=3,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )

      with pytest.raises(httpx.HTTPStatusError) as error_info:
        await arr_client.get_movies({"run_id": "integration-4xx"})

      assert error_info.value.response.status_code == 404
      assert fake_server.request_count("GET", "/api/v3/movie") == 1


@pytest.mark.asyncio
async def test_retryable_5xx_error_retries_then_succeeds() -> None:
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=502, body={"message": "bad_gateway"}),
      ResponseSpec(status_code=200, body=[{"id": 303, "title": "Recovered Movie"}]),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-5xx", ArrType.RADARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=3,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )

      movies = await arr_client.get_movies({"run_id": "integration-5xx"})
      assert movies == [{"id": 303, "title": "Recovered Movie"}]
      assert fake_server.request_count("GET", "/api/v3/movie") == 2


@pytest.mark.asyncio
async def test_timeout_error_retries_then_raises() -> None:
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=200, body=[{"id": 404, "title": "Slow Movie"}], delay_s=0.2),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-timeout", ArrType.RADARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.05,
      )

      with pytest.raises(httpx.TimeoutException):
        await arr_client.get_movies({"run_id": "integration-timeout"})

      assert fake_server.request_count("GET", "/api/v3/movie") == 2


@pytest.mark.asyncio
async def test_scheduler_persists_and_recovers_state_from_previous_file(tmp_path: Path) -> None:
  state_file_path = tmp_path / "state.yaml"
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=200, body=[{"id": 101, "title": "Persisted Movie"}]),
    ],
    ("POST", "/api/v3/command"): [
      ResponseSpec(status_code=200, body={"id": 901, "status": "queued"}),
    ],
  }

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-state-recovery", ArrType.RADARR, fake_server.base_url, 1)
    state_manager = StateManager(FileStateStorage(state_file_path))
    state_manager.load()

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )
      scheduler = Scheduler([target], state_manager, {target.name: arr_client})
      await scheduler.run_once(target)

  assert state_file_path.exists()

  restored_state_manager = StateManager(FileStateStorage(state_file_path))
  restored_state_manager.load()
  restored_target_state = restored_state_manager.get_target_state("integration-state-recovery")

  assert restored_state_manager.state.total_runs == 1
  assert restored_target_state.last_status == RunStatus.SUCCESS
  assert "101" in restored_target_state.items
  assert restored_target_state.items["101"].last_result == "search_triggered"


def test_corrupted_state_file_is_moved_aside(tmp_path: Path) -> None:
  state_file_path = tmp_path / "state.yaml"
  state_file_path.write_text("targets: [not-valid-yaml", encoding="utf-8")

  state_manager = StateManager(FileStateStorage(state_file_path))
  state_manager.load()

  assert state_manager.state.total_runs == 0
  corrupt_files = list(tmp_path.glob(".corrupt.*"))
  assert len(corrupt_files) == 1


@pytest.mark.asyncio
async def test_metrics_endpoint_exposes_target_metrics_after_scheduler_run(tmp_path: Path) -> None:
  responses = {
    ("GET", "/api/v3/movie"): [
      ResponseSpec(status_code=200, body=[{"id": 202, "title": "Metrics Movie"}]),
    ],
    ("POST", "/api/v3/command"): [
      ResponseSpec(status_code=200, body={"id": 902, "status": "queued"}),
    ],
  }
  state_file_path = tmp_path / "metrics-state.yaml"

  with running_fake_arr_server(responses) as fake_server:
    target = create_target("integration-metrics", ArrType.RADARR, fake_server.base_url, 1)
    state_manager = StateManager(FileStateStorage(state_file_path))
    state_manager.load()

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )
      scheduler = Scheduler([target], state_manager, {target.name: arr_client})
      await scheduler.run_once(target)

  web_app = create_web_app()
  test_client = web_app.test_client()

  health_response = test_client.get("/health")
  assert health_response.status_code == 200
  assert health_response.get_data(as_text=True) == "OK"

  metrics_response = test_client.get("/metrics")
  assert metrics_response.status_code == 200

  metrics_text = metrics_response.get_data(as_text=True)
  assert_metric_line(
    metrics_text,
    "gatherarr_run_total",
    ['target="integration-metrics"', 'type="radarr"', 'status="success"'],
  )
  assert_metric_line(
    metrics_text,
    "gatherarr_requests_total",
    ['target="integration-metrics"', 'type="radarr"'],
  )
  assert_metric_line(
    metrics_text,
    "gatherarr_grabs_total",
    ['target="integration-metrics"', 'type="radarr"'],
  )
