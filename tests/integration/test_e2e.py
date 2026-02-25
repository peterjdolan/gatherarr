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
import requests
from openapi_core import OpenAPI
from openapi_core.contrib.requests.requests import RequestsOpenAPIRequest
from openapi_core.contrib.requests.responses import RequestsOpenAPIResponse
from openapi_core.exceptions import OpenAPIError

from app.arr_client import ArrClient
from app.config import ArrTarget, ArrType
from app.http_client import HttpxClient
from app.main import create_web_app
from app.scheduler import MovieId, Scheduler, SeasonId
from app.state import FileStateStorage, RunStatus, StateManager

RouteKey = tuple[str, str]

REPO_ROOT = Path(__file__).resolve().parents[2]
RADARR_SPEC_PATH = REPO_ROOT / "context" / "radarr_api.json"
SONARR_SPEC_PATH = REPO_ROOT / "context" / "sonarr_api.json"
OPENAPI_BASE_URL = "http://localhost:7878"
OPENAPI_API_KEY = "integration-key"
OPENAPI_CONTENT_TYPE = "application/json"


def build_openapi_request(method: str, path: str, body_text: str) -> RequestsOpenAPIRequest:
  """Build an openapi-core request adapter."""
  prepared_request = requests.Request(
    method=method,
    url=f"{OPENAPI_BASE_URL}{path}",
    headers={
      "X-Api-Key": OPENAPI_API_KEY,
      "Content-Type": OPENAPI_CONTENT_TYPE,
    },
    data=body_text,
  ).prepare()
  return RequestsOpenAPIRequest(prepared_request)


def build_openapi_response(status_code: int, body: Any) -> RequestsOpenAPIResponse:
  """Build an openapi-core response adapter."""
  response = requests.Response()
  response.status_code = status_code
  response.headers["Content-Type"] = OPENAPI_CONTENT_TYPE
  response._content = json.dumps(body).encode("utf-8")
  return RequestsOpenAPIResponse(response)


class OpenApiContract:
  """OpenAPI contract helper using openapi-core validators."""

  def __init__(self, service_name: str, spec_path: Path) -> None:
    self.service_name = service_name
    self.spec_path = spec_path
    self.openapi = OpenAPI.from_file_path(str(spec_path))

  def validate_response(self, method: str, path: str, status_code: int, body: Any) -> None:
    """Validate a response body against the operation schema."""
    request = build_openapi_request(method, path, "")
    response = build_openapi_response(status_code, body)
    try:
      self.openapi.validate_response(request, response)
    except OpenAPIError as error:
      raise AssertionError(
        f"{self.service_name} response contract mismatch for {method} {path} {status_code}: {error}"
      ) from error

  def validate_request(self, method: str, path: str, body_text: str) -> None:
    """Validate a request body against the operation schema."""
    request = build_openapi_request(method, path, body_text)
    try:
      self.openapi.validate_request(request)
    except OpenAPIError as error:
      raise AssertionError(
        f"{self.service_name} request contract mismatch for {method} {path}: {error}"
      ) from error


def radarr_contract() -> OpenApiContract:
  """Get the Radarr OpenAPI contract."""
  return OpenApiContract("radarr", RADARR_SPEC_PATH)


def sonarr_contract() -> OpenApiContract:
  """Get the Sonarr OpenAPI contract."""
  return OpenApiContract("sonarr", SONARR_SPEC_PATH)


@dataclass(frozen=True)
class ResponseSpec:
  """Response specification for a fake Arr endpoint."""

  status_code: int
  body: Any
  delay_s: float = 0.0
  enforce_contract: bool = True


@dataclass(frozen=True)
class CapturedRequest:
  """Request data captured by the fake Arr server."""

  method: str
  path: str
  body_text: str


class FakeArrServer:
  """In-process fake Arr HTTP server for integration testing."""

  def __init__(
    self,
    api_contract: OpenApiContract,
    responses: dict[RouteKey, list[ResponseSpec]],
  ) -> None:
    self._api_contract = api_contract
    self._responses = {route: list(route_responses) for route, route_responses in responses.items()}
    self._captured_requests: list[CapturedRequest] = []
    self._lock = threading.Lock()
    self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._build_handler())
    self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
    self._validate_configured_contract()

  def _validate_configured_contract(self) -> None:
    """Validate fake server response fixtures against OpenAPI contracts."""
    for (method, path), configured_responses in self._responses.items():
      self._api_contract.validate_request(method, path, "")
      for response in configured_responses:
        if response.enforce_contract:
          self._api_contract.validate_response(
            method=method,
            path=path,
            status_code=response.status_code,
            body=response.body,
          )

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
    server_address = self._server.server_address
    raw_host = server_address[0]
    port = server_address[1]
    host = raw_host.decode("utf-8") if isinstance(raw_host, bytes) else raw_host
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
  api_contract: OpenApiContract,
  responses: dict[RouteKey, list[ResponseSpec]],
) -> Iterator[FakeArrServer]:
  """Run a fake Arr server for the duration of the context."""
  server = FakeArrServer(api_contract, responses)
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

  with running_fake_arr_server(radarr_contract(), responses) as fake_server:
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
      ResponseSpec(
        status_code=200,
        body=[
          {
            "id": 22,
            "title": "Integration Series",
            "seasons": [{"seasonNumber": 1}, {"seasonNumber": 2}],
          }
        ],
      ),
    ],
    ("POST", "/api/v3/command"): [
      ResponseSpec(status_code=200, body={"id": 601, "status": "queued"}),
    ],
  }

  with running_fake_arr_server(sonarr_contract(), responses) as fake_server:
    target = create_target("integration-sonarr-success", ArrType.SONARR, fake_server.base_url, 1)

    async with httpx.AsyncClient() as async_http_client:
      arr_client = ArrClient(
        target=target,
        http_client=HttpxClient(async_http_client),
        max_retries=2,
        retry_delay_s=0.01,
        timeout_s=0.5,
      )

      seasons = await arr_client.get_seasons({"run_id": "integration-sonarr-success"})
      assert seasons == [
        {"seriesId": 22, "seriesTitle": "Integration Series", "seasonNumber": 1},
        {"seriesId": 22, "seriesTitle": "Integration Series", "seasonNumber": 2},
      ]

      command_result = await arr_client.search_season(
        SeasonId(series_id=22, season_number=1, series_name="Integration Series"),
        {"run_id": "integration-sonarr-success"},
      )
      assert command_result == {"id": 601, "status": "queued"}

    assert fake_server.request_count("GET", "/api/v3/series") == 1
    command_requests = fake_server.requests_for("POST", "/api/v3/command")
    assert len(command_requests) == 1
    assert json.loads(command_requests[0].body_text) == {
      "name": "SeasonSearch",
      "seriesId": 22,
      "seasonNumber": 1,
    }


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

  with running_fake_arr_server(radarr_contract(), responses) as fake_server:
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

  with running_fake_arr_server(radarr_contract(), responses) as fake_server:
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
