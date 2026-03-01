"""Tests for main module."""

import app.main as main_module
from app.main import create_web_app, main, setup_logging, start_web_server


class TestMainModule:
  def test_can_import_main_module(self) -> None:
    """Test that the main module can be successfully imported."""
    assert main_module is not None

  def test_main_function_exists(self) -> None:
    """Test that the main function exists and is callable."""
    assert callable(main)

  def test_setup_logging_function_exists(self) -> None:
    """Test that the setup_logging function exists and is callable."""
    assert callable(setup_logging)

  def test_create_web_app_function_exists(self) -> None:
    """Test that the create_web_app function exists and is callable."""
    assert callable(create_web_app)

  def test_start_web_server_function_exists(self) -> None:
    """Test that the start_web_server function exists and is callable."""
    assert callable(start_web_server)

  def test_health_endpoint_always_available(self) -> None:
    """Health endpoint is served regardless of metrics_enabled."""
    app = create_web_app(metrics_enabled=False)
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "OK"

  def test_metrics_endpoint_404_when_disabled(self) -> None:
    """Metrics endpoint returns 404 when metrics_enabled is False."""
    app = create_web_app(metrics_enabled=False)
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 404

  def test_metrics_endpoint_available_when_enabled(self) -> None:
    """Metrics endpoint is served when metrics_enabled is True."""
    app = create_web_app(metrics_enabled=True)
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
