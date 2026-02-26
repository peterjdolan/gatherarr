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
