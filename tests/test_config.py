"""Tests for configuration module."""

import os
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.config import ArrTarget, ArrType, Config, TargetOverrideSettings, load_config


class TestLogLevelParsing:
  @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
  def test_valid_log_levels(self, level: str) -> None:
    """Test all valid log levels are parsed correctly."""
    config = Config(log_level=level, state_file_path=None)
    assert config.log_level == level

  @pytest.mark.parametrize(
    "input_level,expected",
    [
      ("debug", "DEBUG"),
      ("Debug", "DEBUG"),
      ("DEBUG", "DEBUG"),
      ("info", "INFO"),
      ("Info", "INFO"),
      ("INFO", "INFO"),
      ("warning", "WARNING"),
      ("Warning", "WARNING"),
      ("WARNING", "WARNING"),
      ("error", "ERROR"),
      ("Error", "ERROR"),
      ("ERROR", "ERROR"),
      ("critical", "CRITICAL"),
      ("Critical", "CRITICAL"),
      ("CRITICAL", "CRITICAL"),
    ],
  )
  def test_case_insensitive(self, input_level: str, expected: str) -> None:
    """Test log level parsing is case insensitive."""
    config = Config(log_level=input_level, state_file_path=None)
    assert config.log_level == expected

  @pytest.mark.parametrize("level", ["warn", "Warn", "WARN", "WARNING"])
  def test_warn_normalized_to_warning(self, level: str) -> None:
    """Test that WARN is normalized to WARNING."""
    config = Config(log_level=level, state_file_path=None)
    assert config.log_level == "WARNING"

  @pytest.mark.parametrize("level", ["invalid", "TRACE", "VERBOSE", "unknown"])
  def test_invalid_log_level_defaults_to_info(self, level: str) -> None:
    """Test that invalid log levels default to INFO."""
    config = Config(log_level=level, state_file_path=None)
    assert config.log_level == "INFO"

  @pytest.mark.parametrize("level", ["", "   "])
  def test_empty_log_level_raises_error(self, level: str) -> None:
    """Test that empty log level raises ValidationError."""
    with pytest.raises(ValidationError, match="log_level must be non-empty"):
      Config(log_level=level)

  @pytest.mark.parametrize(
    "env_value,expected",
    [
      ("debug", "DEBUG"),
      ("INFO", "INFO"),
      ("warning", "WARNING"),
      ("error", "ERROR"),
      ("critical", "CRITICAL"),
      ("warn", "WARNING"),
      ("invalid", "INFO"),
    ],
  )
  def test_log_level_from_env(self, env_value: str, expected: str) -> None:
    """Test log level parsing from environment variables."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_LOG_LEVEL": env_value,
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    config = load_config(env)
    assert config.log_level == expected
    assert config.state_file_path is None

  def test_default_log_level(self) -> None:
    """Test that default log level is INFO."""
    config = Config(state_file_path=None)
    assert config.log_level == "INFO"


class TestLoadConfig:
  def test_load_minimal_config(self) -> None:
    env = {
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    config = load_config(env)
    assert len(config.targets) == 1
    assert config.targets[0].name == "test"
    assert config.targets[0].arr_type == ArrType.RADARR
    assert config.targets[0].base_url == "http://localhost:7878"
    assert config.targets[0].api_key == "test-key"
    assert config.log_level == "INFO"
    assert config.metrics_enabled is True
    assert config.metrics_port == 9090

  def test_load_config_with_overrides(self) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "custom_state.yaml"
      env = {
        "GTH_LOG_LEVEL": "debug",
        "GTH_METRICS_ENABLED": "false",
        "GTH_METRICS_PORT": "8080",
        "GTH_STATE_FILE_PATH": str(state_path),
        "GTH_OPS_PER_INTERVAL": "5",
        "GTH_INTERVAL_S": "120",
        "GTH_ARR_0_TYPE": "sonarr",
        "GTH_ARR_0_NAME": "sonarr1",
        "GTH_ARR_0_BASEURL": "http://sonarr:8989",
        "GTH_ARR_0_APIKEY": "key1",
        "GTH_ARR_0_OPS_PER_INTERVAL": "10",
        "GTH_ARR_0_INTERVAL_S": "300",
      }
      config = load_config(env)
      assert config.log_level == "DEBUG"
      assert config.metrics_enabled is False
      assert config.metrics_port == 8080
      assert config.state_file_path == str(state_path)
      assert config.ops_per_interval == 5
      assert config.interval_s == 120
      assert config.targets[0].ops_per_interval == 10
      assert config.targets[0].interval_s == 300

  def test_load_multiple_targets(self) -> None:
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "radarr1",
      "GTH_ARR_0_BASEURL": "http://radarr1:7878",
      "GTH_ARR_0_APIKEY": "key1",
      "GTH_ARR_1_TYPE": "sonarr",
      "GTH_ARR_1_NAME": "sonarr1",
      "GTH_ARR_1_BASEURL": "http://sonarr1:8989",
      "GTH_ARR_1_APIKEY": "key2",
    }
    config = load_config(env)
    assert len(config.targets) == 2
    assert config.targets[0].name == "radarr1"
    assert config.targets[1].name == "sonarr1"

  def test_load_config_missing_required_raises(self) -> None:
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
    }
    with pytest.raises(ValueError, match="Missing required config"):
      load_config(env)

  def test_load_config_no_targets_raises(self) -> None:
    env: dict[str, str] = {"GTH_STATE_FILE_PATH": ""}
    with pytest.raises(ValueError, match="At least one"):
      load_config(env)

  def test_load_config_invalid_arr_type_raises(self) -> None:
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "invalid",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValueError, match="Invalid arr type"):
      load_config(env)


class TestArrTarget:
  def test_valid_arr_target(self) -> None:
    """Test creating a valid ArrTarget."""
    target = ArrTarget(
      name="test",
      arr_type=ArrType.RADARR,
      base_url="http://localhost:7878",
      api_key="test-key",
      ops_per_interval=1,
      interval_s=60,
      item_revisit_timeout_s=3600,
    )
    assert target.name == "test"
    assert target.arr_type == ArrType.RADARR
    assert target.base_url == "http://localhost:7878"

  def test_arr_target_validates_url(self) -> None:
    """Test that ArrTarget validates base_url is a valid URL."""
    with pytest.raises(ValidationError) as exc_info:
      ArrTarget(
        name="test",
        arr_type=ArrType.RADARR,
        base_url="invalid-url",
        api_key="test-key",
        ops_per_interval=1,
        interval_s=60,
        item_revisit_timeout_s=3600,
      )
    assert "base_url must be a valid URL" in str(exc_info.value)

  def test_arr_target_validates_url_scheme(self) -> None:
    """Test that ArrTarget validates URL scheme is http or https."""
    with pytest.raises(ValidationError) as exc_info:
      ArrTarget(
        name="test",
        arr_type=ArrType.RADARR,
        base_url="ftp://localhost:7878",
        api_key="test-key",
        ops_per_interval=1,
        interval_s=60,
        item_revisit_timeout_s=3600,
      )
    assert "base_url must use http or https scheme" in str(exc_info.value)

  @pytest.mark.parametrize(
    "ops_per_interval,interval_s,item_revisit_timeout_s",
    [
      (0, 60, 3600),
      (1, 0, 3600),
      (1, 60, 0),
    ],
  )
  def test_arr_target_validates_positive_integers(
    self, ops_per_interval: int, interval_s: int, item_revisit_timeout_s: int
  ) -> None:
    """Test that ArrTarget validates positive integer fields."""
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
      ArrTarget(
        name="test",
        arr_type=ArrType.RADARR,
        base_url="http://localhost:7878",
        api_key="test-key",
        ops_per_interval=ops_per_interval,
        interval_s=interval_s,
        item_revisit_timeout_s=item_revisit_timeout_s,
      )

  @pytest.mark.parametrize("name", ["", "   "])
  def test_arr_target_validates_non_empty_name(self, name: str) -> None:
    """Test that ArrTarget validates name is non-empty."""
    with pytest.raises(ValidationError) as exc_info:
      ArrTarget(
        name=name,
        arr_type=ArrType.RADARR,
        base_url="http://localhost:7878",
        api_key="test-key",
        ops_per_interval=1,
        interval_s=60,
        item_revisit_timeout_s=3600,
      )
    assert "name must be non-empty" in str(exc_info.value)

  @pytest.mark.parametrize("api_key", ["", "   "])
  def test_arr_target_validates_non_empty_api_key(self, api_key: str) -> None:
    """Test that ArrTarget validates api_key is non-empty."""
    with pytest.raises(ValidationError) as exc_info:
      ArrTarget(
        name="test",
        arr_type=ArrType.RADARR,
        base_url="http://localhost:7878",
        api_key=api_key,
        ops_per_interval=1,
        interval_s=60,
        item_revisit_timeout_s=3600,
      )
    assert "api_key must be non-empty" in str(exc_info.value)

  def test_arr_target_accepts_https_url(self) -> None:
    """Test that ArrTarget accepts https URLs."""
    target = ArrTarget(
      name="test",
      arr_type=ArrType.SONARR,
      base_url="https://example.com:8989",
      api_key="test-key",
      ops_per_interval=1,
      interval_s=60,
      item_revisit_timeout_s=3600,
    )
    assert target.base_url == "https://example.com:8989"


class TestConfigValidation:
  def test_config_validates_state_file_path_writable(self) -> None:
    """Test that Config validates state_file_path is writable."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      config = Config(state_file_path=str(state_path))
      assert config.state_file_path == str(state_path)

  @pytest.mark.parametrize("state_file_path", ["", "   "])
  def test_config_validates_state_file_path_non_empty(self, state_file_path: str) -> None:
    """Test that Config converts empty state_file_path to None."""
    config = Config(state_file_path=state_file_path)
    assert config.state_file_path is None

  def test_config_validates_state_file_path_parent_exists(self) -> None:
    """Test that Config validates state_file_path parent directory exists."""
    with pytest.raises(ValidationError) as exc_info:
      Config(state_file_path="/nonexistent/path/state.yaml")
    assert "parent directory does not exist" in str(exc_info.value)

  def test_config_validates_state_file_path_existing_file_writable(self) -> None:
    """Test that Config validates existing state_file_path is writable."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      state_path.touch()
      # Make it read-only (if possible on this system)
      try:
        state_path.chmod(0o444)
        with pytest.raises(ValidationError) as exc_info:
          Config(state_file_path=str(state_path))
        assert "not writable" in str(exc_info.value)
      except OSError, PermissionError:
        # On some systems we can't make files read-only, skip this test
        pass
      finally:
        # Restore permissions for cleanup
        try:
          state_path.chmod(0o644)
        except OSError, PermissionError:
          pass

  @pytest.mark.parametrize("invalid_port", [0, -1])
  def test_config_validates_metrics_port_positive(self, invalid_port: int) -> None:
    """Test that Config validates metrics_port is positive."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      with pytest.raises(ValidationError):
        Config(metrics_port=invalid_port, state_file_path=str(state_path))

  def test_config_validates_metrics_port_valid(self) -> None:
    """Test that Config accepts valid metrics_port."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      config = Config(metrics_port=9090, state_file_path=str(state_path))
      assert config.metrics_port == 9090

  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_config_validates_ops_per_interval_positive(self, invalid_value: int) -> None:
    """Test that Config validates ops_per_interval is positive."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      with pytest.raises(ValidationError):
        Config(ops_per_interval=invalid_value, state_file_path=str(state_path))

  def test_config_validates_ops_per_interval_valid(self) -> None:
    """Test that Config accepts valid ops_per_interval."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      config = Config(ops_per_interval=5, state_file_path=str(state_path))
      assert config.ops_per_interval == 5

  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_config_validates_interval_s_positive(self, invalid_value: int) -> None:
    """Test that Config validates interval_s is positive."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      with pytest.raises(ValidationError):
        Config(interval_s=invalid_value, state_file_path=str(state_path))

  def test_config_validates_interval_s_valid(self) -> None:
    """Test that Config accepts valid interval_s."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      config = Config(interval_s=120, state_file_path=str(state_path))
      assert config.interval_s == 120

  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_config_validates_item_revisit_s_positive(self, invalid_value: int) -> None:
    """Test that Config validates item_revisit_s is positive."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      with pytest.raises(ValidationError):
        Config(item_revisit_s=invalid_value, state_file_path=str(state_path))

  def test_config_validates_item_revisit_s_valid(self) -> None:
    """Test that Config accepts valid item_revisit_s."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      config = Config(item_revisit_s=86400, state_file_path=str(state_path))
      assert config.item_revisit_s == 86400


class TestTargetOverrideSettings:
  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_target_override_validates_ops_per_interval_positive(self, invalid_value: int) -> None:
    """Test that TargetOverrideSettings validates ops_per_interval is positive."""
    with pytest.raises(ValidationError):
      TargetOverrideSettings(ops_per_interval=invalid_value)

  def test_target_override_validates_ops_per_interval_valid(self) -> None:
    """Test that TargetOverrideSettings accepts valid ops_per_interval."""
    settings = TargetOverrideSettings(ops_per_interval=10)
    assert settings.ops_per_interval == 10

  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_target_override_validates_interval_s_positive(self, invalid_value: int) -> None:
    """Test that TargetOverrideSettings validates interval_s is positive."""
    with pytest.raises(ValidationError):
      TargetOverrideSettings(interval_s=invalid_value)

  def test_target_override_validates_interval_s_valid(self) -> None:
    """Test that TargetOverrideSettings accepts valid interval_s."""
    settings = TargetOverrideSettings(interval_s=300)
    assert settings.interval_s == 300

  @pytest.mark.parametrize("invalid_value", [0, -1])
  def test_target_override_validates_item_revisit_timeout_s_positive(
    self, invalid_value: int
  ) -> None:
    """Test that TargetOverrideSettings validates item_revisit_timeout_s is positive."""
    with pytest.raises(ValidationError):
      TargetOverrideSettings(item_revisit_timeout_s=invalid_value)

  def test_target_override_validates_item_revisit_timeout_s_valid(self) -> None:
    """Test that TargetOverrideSettings accepts valid item_revisit_timeout_s."""
    settings = TargetOverrideSettings(item_revisit_timeout_s=7200)
    assert settings.item_revisit_timeout_s == 7200

  def test_target_override_allows_none(self) -> None:
    """Test that TargetOverrideSettings allows None values."""
    settings = TargetOverrideSettings()
    assert settings.ops_per_interval is None
    assert settings.interval_s is None
    assert settings.item_revisit_timeout_s is None


class TestLoadConfigValidation:
  def test_load_config_validates_arr_target_url(self) -> None:
    """Test that load_config validates ArrTarget URLs."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "invalid-url",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValueError, match="base_url must be a valid URL"):
      load_config(env)

  @pytest.mark.parametrize(
    "env_key,env_value",
    [
      ("GTH_ARR_0_OPS_PER_INTERVAL", "0"),
      ("GTH_ARR_0_INTERVAL_S", "-1"),
      ("GTH_ARR_0_ITEM_REVISIT_TIMEOUT_S", "0"),
    ],
  )
  def test_load_config_validates_arr_target_positive_integers(
    self, env_key: str, env_value: str
  ) -> None:
    """Test that load_config validates ArrTarget positive integer fields."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
      env_key: env_value,
    }
    with pytest.raises(ValidationError):
      load_config(env)

  def test_load_config_validates_arr_target_non_empty_name(self) -> None:
    """Test that load_config validates ArrTarget name is non-empty."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValidationError) as exc_info:
      load_config(env)
    assert "name must be non-empty" in str(exc_info.value)

  def test_load_config_validates_arr_target_non_empty_api_key(self) -> None:
    """Test that load_config validates ArrTarget api_key is non-empty."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "",
    }
    with pytest.raises(ValidationError) as exc_info:
      load_config(env)
    assert "api_key must be non-empty" in str(exc_info.value)

  def test_load_config_validates_config_ops_per_interval_positive(self) -> None:
    """Test that load_config validates Config ops_per_interval is positive."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_OPS_PER_INTERVAL": "0",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
      load_config(env)

  def test_load_config_validates_config_interval_s_positive(self) -> None:
    """Test that load_config validates Config interval_s is positive."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_INTERVAL_S": "-1",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
      load_config(env)

  def test_load_config_validates_config_metrics_port_positive(self) -> None:
    """Test that load_config validates Config metrics_port is positive."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_METRICS_PORT": "0",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "test",
      "GTH_ARR_0_BASEURL": "http://localhost:7878",
      "GTH_ARR_0_APIKEY": "test-key",
    }
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
      load_config(env)

  def test_load_config_validates_all_targets(self) -> None:
    """Test that load_config validates all targets, not just the first."""
    # Save and clear potentially conflicting env vars
    saved_env = {}
    for key in ["GTH_METRICS_PORT", "GTH_OPS_PER_INTERVAL", "GTH_INTERVAL_S"]:
      if key in os.environ:
        saved_env[key] = os.environ.pop(key)

    try:
      env = {
        "GTH_STATE_FILE_PATH": "",
        "GTH_ARR_0_TYPE": "radarr",
        "GTH_ARR_0_NAME": "radarr1",
        "GTH_ARR_0_BASEURL": "http://radarr1:7878",
        "GTH_ARR_0_APIKEY": "key1",
        "GTH_ARR_1_TYPE": "sonarr",
        "GTH_ARR_1_NAME": "sonarr1",
        "GTH_ARR_1_BASEURL": "invalid-url",
        "GTH_ARR_1_APIKEY": "key2",
      }
      with pytest.raises(ValidationError) as exc_info:
        load_config(env)
      assert "base_url must be a valid URL" in str(exc_info.value)
    finally:
      # Restore saved env vars
      os.environ.update(saved_env)

  def test_load_config_validates_missing_name_after_type(self) -> None:
    """Test that load_config validates missing name when type is present."""
    # Save and clear potentially conflicting env vars
    saved_env = {}
    for key in ["GTH_METRICS_PORT", "GTH_OPS_PER_INTERVAL", "GTH_INTERVAL_S"]:
      if key in os.environ:
        saved_env[key] = os.environ.pop(key)

    try:
      env = {
        "GTH_STATE_FILE_PATH": "",
        "GTH_ARR_0_TYPE": "radarr",
        "GTH_ARR_0_BASEURL": "http://localhost:7878",
        "GTH_ARR_0_APIKEY": "test-key",
      }
      with pytest.raises(ValueError) as exc_info:
        load_config(env)
      assert "Missing required config: GTH_ARR_0_NAME" in str(exc_info.value)
    finally:
      os.environ.update(saved_env)

  def test_load_config_validates_missing_baseurl_after_name(self) -> None:
    """Test that load_config validates missing baseurl when name is present."""
    # Save and clear potentially conflicting env vars
    saved_env = {}
    for key in ["GTH_METRICS_PORT", "GTH_OPS_PER_INTERVAL", "GTH_INTERVAL_S"]:
      if key in os.environ:
        saved_env[key] = os.environ.pop(key)

    try:
      env = {
        "GTH_STATE_FILE_PATH": "",
        "GTH_ARR_0_TYPE": "radarr",
        "GTH_ARR_0_NAME": "test",
        "GTH_ARR_0_APIKEY": "test-key",
      }
      with pytest.raises(ValueError) as exc_info:
        load_config(env)
      assert "Missing required config: GTH_ARR_0_BASEURL" in str(exc_info.value)
    finally:
      os.environ.update(saved_env)

  def test_load_config_validates_missing_apikey_after_baseurl(self) -> None:
    """Test that load_config validates missing apikey when baseurl is present."""
    # Save and clear potentially conflicting env vars
    saved_env = {}
    for key in ["GTH_METRICS_PORT", "GTH_OPS_PER_INTERVAL", "GTH_INTERVAL_S"]:
      if key in os.environ:
        saved_env[key] = os.environ.pop(key)

    try:
      env = {
        "GTH_STATE_FILE_PATH": "",
        "GTH_ARR_0_TYPE": "radarr",
        "GTH_ARR_0_NAME": "test",
        "GTH_ARR_0_BASEURL": "http://localhost:7878",
      }
      with pytest.raises(ValueError) as exc_info:
        load_config(env)
      assert "Missing required config: GTH_ARR_0_APIKEY" in str(exc_info.value)
    finally:
      os.environ.update(saved_env)
