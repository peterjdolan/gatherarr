"""Main application entry point."""

import asyncio
import logging
import signal
import sys
import threading

import httpx
import structlog
from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.arr_client import ArrClient
from app.config import load_config
from app.http_client import HttpxClient
from app.log_redaction import redact_sensitive_fields
from app.scheduler import Scheduler
from app.startup_banner import format_banner
from app.state import FileStateStorage, InMemoryStateStorage, StateManager, StateStorage

logger = structlog.get_logger()


def setup_logging(log_level: str) -> None:
  """Configure structured logging."""
  try:
    numeric_level = getattr(logging, log_level.upper())
  except AttributeError:
    raise ValueError(f"Invalid log level: {log_level}")
  logging.basicConfig(level=numeric_level)

  structlog.configure(
    processors=[
      structlog.processors.TimeStamper(fmt="iso"),
      structlog.processors.add_log_level,
      redact_sensitive_fields,
      structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
  )


def create_web_app() -> Flask:
  """Create and configure the Flask application for metrics."""
  app = Flask(__name__)

  @app.route("/health")
  def health_handler() -> Response:
    """Health check endpoint."""
    return Response("OK", mimetype="text/plain")

  @app.route("/metrics")
  def metrics_handler() -> Response:
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

  return app


def start_web_server(address: str, port: int) -> threading.Thread:
  """Start the Flask web server for metrics and health endpoints in a separate thread."""
  app = create_web_app()

  def run_server() -> None:
    app.run(host=address, port=port, threaded=True, use_reloader=False)

  server_thread = threading.Thread(target=run_server, daemon=True)
  server_thread.start()
  logger.debug("HTTP server started", address=address, port=port)
  return server_thread


async def main() -> None:
  """Main entry point."""
  try:
    config = load_config()
  except ValueError as e:
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)

  setup_logging(config.log_level)
  logger.info(format_banner(config))
  logger.debug(
    "Configuration loaded and logging configured",
    targets=len(config.targets),
    metrics_enabled=config.metrics_enabled,
    log_level=config.log_level,
    config=config,
  )

  logger.debug(
    "Starting Gatherarr",
    targets=len(config.targets),
    metrics_enabled=config.metrics_enabled,
  )

  logger.debug("Initializing state storage", state_file_path=config.state_file_path)
  if config.state_file_path is None:
    storage: StateStorage = InMemoryStateStorage()
    logger.debug("Using in-memory state storage")
  else:
    storage = FileStateStorage(config.state_file_path)
    logger.debug("Using file-based state storage", state_file_path=config.state_file_path)
  state_manager = StateManager(storage)
  logger.debug("Loading state")
  state_manager.load()
  logger.debug("State loaded", targets=len(state_manager.state.targets))

  http_client_instance = httpx.AsyncClient()
  http_client = HttpxClient(http_client_instance)

  arr_clients: dict[str, ArrClient] = {}
  for target in config.targets:
    arr_clients[target.name] = ArrClient(
      target=target,
      http_client=http_client,
    )

  scheduler = Scheduler(config.targets, state_manager, arr_clients)
  logger.debug("Starting scheduler task")
  scheduler_task = asyncio.create_task(scheduler.start())

  if config.metrics_enabled:
    start_web_server(config.metrics_address, config.metrics_port)
  else:
    logger.debug("Metrics disabled, skipping web server")

  shutdown_event = asyncio.Event()

  def signal_handler() -> None:
    logger.debug("Received shutdown signal")
    shutdown_event.set()

  loop = asyncio.get_event_loop()
  for sig in (signal.SIGTERM, signal.SIGINT):
    loop.add_signal_handler(sig, signal_handler)

  try:
    await shutdown_event.wait()
  except KeyboardInterrupt:
    pass
  finally:
    logger.debug(
      "Shutting down...",
      shutdown_timeout_s=config.shutdown_timeout_s,
    )
    logger.debug("Stopping scheduler")
    scheduler.stop()
    try:
      await asyncio.wait_for(scheduler_task, timeout=config.shutdown_timeout_s)
      logger.debug("Scheduler stopped gracefully")
    except asyncio.TimeoutError:
      logger.debug(
        "Scheduler did not stop within timeout, cancelling",
        shutdown_timeout_s=config.shutdown_timeout_s,
      )
      scheduler_task.cancel()
      try:
        await scheduler_task
      except asyncio.CancelledError:
        logger.debug("Scheduler task cancelled")
    except asyncio.CancelledError:
      logger.debug("Scheduler task cancelled")

    logger.debug("Closing HTTP client")
    await http_client_instance.aclose()
    logger.debug("HTTP client closed")

    logger.debug("Application shutdown complete")


if __name__ == "__main__":
  asyncio.run(main())
