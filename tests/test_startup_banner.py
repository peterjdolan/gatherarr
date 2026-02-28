"""Tests for startup banner module."""

import tempfile
from pathlib import Path

from app.config import ArrTarget, ArrType, Config, TargetSettings, load_config
from app.startup_banner import REDACTED, format_banner


class TestFormatBanner:
  def test_banner_includes_global_config(self) -> None:
    """Banner displays all global configuration values."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_LOG_LEVEL": "debug",
      "GTH_METRICS_ENABLED": "false",
      "GTH_METRICS_ADDRESS": "127.0.0.1",
      "GTH_METRICS_PORT": "8080",
      "GTH_OPS_PER_INTERVAL": "5",
      "GTH_INTERVAL_S": "120",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "Radarr",
      "GTH_ARR_0_BASEURL": "http://radarr:7878",
      "GTH_ARR_0_APIKEY": "secret-key",
    }
    config = load_config(env)
    banner = format_banner(config)
    assert "=== Gatherarr Startup Configuration ===" in banner
    assert "log_level: DEBUG" in banner
    assert "metrics_enabled: False" in banner
    assert "metrics_address: 127.0.0.1" in banner
    assert "metrics_port: 8080" in banner
    assert "state_file_path: (in-memory)" in banner
    assert "ops_per_interval: 5" in banner
    assert "interval_s: 120" in banner

  def test_banner_redacts_api_key(self) -> None:
    """Banner never displays API key values."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "Radarr",
      "GTH_ARR_0_BASEURL": "http://radarr:7878",
      "GTH_ARR_0_APIKEY": "super-secret-api-key-12345",
    }
    config = load_config(env)
    banner = format_banner(config)
    assert "super-secret-api-key-12345" not in banner
    assert REDACTED in banner
    assert "api_key: [REDACTED]" in banner

  def test_banner_includes_per_target_config(self) -> None:
    """Banner displays per-target configuration with resolved settings."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "Radarr",
      "GTH_ARR_0_BASEURL": "http://radarr:7878",
      "GTH_ARR_0_APIKEY": "key1",
      "GTH_ARR_0_OPS_PER_INTERVAL": "10",
      "GTH_ARR_0_INTERVAL_S": "300",
      "GTH_ARR_1_TYPE": "sonarr",
      "GTH_ARR_1_NAME": "Sonarr",
      "GTH_ARR_1_BASEURL": "http://sonarr:8989",
      "GTH_ARR_1_APIKEY": "key2",
    }
    config = load_config(env)
    banner = format_banner(config)
    assert "[0] Radarr (radarr)" in banner
    assert "base_url: http://radarr:7878" in banner
    assert "ops_per_interval: 10" in banner
    assert "interval_s: 300" in banner
    assert "[1] Sonarr (sonarr)" in banner
    assert "base_url: http://sonarr:8989" in banner

  def test_banner_includes_eligibility_settings(self) -> None:
    """Banner displays eligibility and tag filtering settings."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_REQUIRE_MONITORED": "false",
      "GTH_REQUIRE_CUTOFF_UNMET": "false",
      "GTH_RELEASED_ONLY": "true",
      "GTH_INCLUDE_TAGS": "4k, anime",
      "GTH_EXCLUDE_TAGS": "paused",
      "GTH_ARR_0_TYPE": "sonarr",
      "GTH_ARR_0_NAME": "Sonarr",
      "GTH_ARR_0_BASEURL": "http://sonarr:8989",
      "GTH_ARR_0_APIKEY": "key",
      "GTH_ARR_0_INCLUDE_TAGS": "anime",
      "GTH_ARR_0_EXCLUDE_TAGS": "blocked",
      "GTH_ARR_0_MIN_MISSING_EPISODES": "3",
      "GTH_ARR_0_MIN_MISSING_PERCENT": "20.5",
    }
    config = load_config(env)
    banner = format_banner(config)
    assert "require_monitored: False" in banner
    assert "require_cutoff_unmet: False" in banner
    assert "released_only: True" in banner
    assert "include_tags: anime" in banner
    assert "exclude_tags: blocked" in banner
    assert "min_missing_episodes: 3" in banner
    assert "min_missing_percent: 20.5" in banner

  def test_banner_formats_empty_tags_as_none(self) -> None:
    """Banner displays (none) for empty tag sets."""
    env = {
      "GTH_STATE_FILE_PATH": "",
      "GTH_INCLUDE_TAGS": "",
      "GTH_EXCLUDE_TAGS": "",
      "GTH_ARR_0_TYPE": "radarr",
      "GTH_ARR_0_NAME": "Radarr",
      "GTH_ARR_0_BASEURL": "http://radarr:7878",
      "GTH_ARR_0_APIKEY": "key",
    }
    config = load_config(env)
    banner = format_banner(config)
    assert "include_tags: (none)" in banner
    assert "exclude_tags: (none)" in banner

  def test_banner_formats_state_file_path(self) -> None:
    """Banner displays state file path or (in-memory) when None."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      env = {
        "GTH_STATE_FILE_PATH": str(state_path),
        "GTH_ARR_0_TYPE": "radarr",
        "GTH_ARR_0_NAME": "Radarr",
        "GTH_ARR_0_BASEURL": "http://radarr:7878",
        "GTH_ARR_0_APIKEY": "key",
      }
      config = load_config(env)
      banner = format_banner(config)
      assert f"state_file_path: {state_path}" in banner

  def test_banner_with_direct_config(self) -> None:
    """Banner works with directly constructed Config and ArrTarget."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      settings = TargetSettings(
        ops_per_interval=1,
        interval_s=60,
        item_revisit_s=604800,
      )
      target = ArrTarget(
        name="TestRadarr",
        arr_type=ArrType.RADARR,
        base_url="http://localhost:7878",
        api_key="secret",
        settings=settings,
      )
      config = Config(state_file_path=str(state_path))
      config.targets = [target]
      banner = format_banner(config)
      assert "[0] TestRadarr (radarr)" in banner
      assert "http://localhost:7878" in banner
      assert "secret" not in banner
      assert REDACTED in banner
