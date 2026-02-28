"""Configuration loading and validation from environment variables."""

import ipaddress
import logging
import os
import re
from enum import StrEnum
from pathlib import Path
from typing import TypeVar
from urllib.parse import urlparse

import structlog
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.tag_utils import coerce_tag_set

logger = structlog.get_logger()
_OverrideValue = TypeVar("_OverrideValue")

_TARGET_OVERRIDE_ENV_MAP: tuple[tuple[str, str], ...] = (
  ("OPS_PER_INTERVAL", "ops_per_interval"),
  ("INTERVAL_S", "interval_s"),
  ("ITEM_REVISIT_S", "item_revisit_s"),
  ("REQUIRE_MONITORED", "require_monitored"),
  ("REQUIRE_CUTOFF_UNMET", "require_cutoff_unmet"),
  ("RELEASED_ONLY", "released_only"),
  ("SEARCH_BACKOFF_S", "search_backoff_s"),
  ("DRY_RUN", "dry_run"),
  ("INCLUDE_TAGS", "include_tags"),
  ("EXCLUDE_TAGS", "exclude_tags"),
  ("MIN_MISSING_EPISODES", "min_missing_episodes"),
  ("MIN_MISSING_PERCENT", "min_missing_percent"),
)


def _resolve_override_value(
  override_value: _OverrideValue | None, default_value: _OverrideValue
) -> _OverrideValue:
  """Resolve an optional override value against a default."""
  return default_value if override_value is None else override_value


class TargetSettings(BaseModel):
  """Resolved settings for target-level behavior."""

  ops_per_interval: int = Field(ge=1)
  interval_s: int = Field(ge=1)
  item_revisit_s: int = Field(ge=1)
  require_monitored: bool = True
  require_cutoff_unmet: bool = True
  released_only: bool = False
  search_backoff_s: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: set[str] = Field(default_factory=set)
  exclude_tags: set[str] = Field(default_factory=set)
  min_missing_episodes: int = Field(default=0, ge=0)
  min_missing_percent: float = Field(default=0.0, ge=0.0, le=100.0)

  @field_validator("include_tags", "exclude_tags", mode="before")
  @classmethod
  def normalize_tags(cls, v: object) -> set[str]:
    """Normalize include/exclude tags from CSV or iterable values."""
    return coerce_tag_set(v)


def _collect_target_override_data(env_dict: dict[str, str], index: int) -> dict[str, str]:
  """Collect raw target override values from environment."""
  override_data: dict[str, str] = {}
  target_prefix = f"GTH_ARR_{index}_"
  for env_suffix, override_field in _TARGET_OVERRIDE_ENV_MAP:
    env_key = f"{target_prefix}{env_suffix}"
    env_value = env_dict.get(env_key)
    if env_value is not None:
      override_data[override_field] = env_value
  return override_data


def _parse_int_override(value: str | None, default: int) -> int:
  """Parse an integer override value."""
  if value is None:
    return default
  try:
    return int(value)
  except (ValueError, TypeError) as e:
    raise ValueError(f"Invalid integer value: {value}") from e


def _parse_bool_override(value: str | None, default: bool) -> bool:
  """Parse a boolean override value."""
  if value is None:
    return default
  lower = value.lower().strip()
  if lower in ("true", "1", "yes", "on"):
    return True
  if lower in ("false", "0", "no", "off"):
    return False
  raise ValueError(f"Invalid boolean value: {value}")


def _parse_float_override(value: str | None, default: float) -> float:
  """Parse a float override value."""
  if value is None:
    return default
  try:
    return float(value)
  except (ValueError, TypeError) as e:
    raise ValueError(f"Invalid float value: {value}") from e


def _build_target_settings(base_config: "Config", override_data: dict[str, str]) -> TargetSettings:
  """Build resolved target settings from defaults and per-target overrides."""
  include_tags_raw = (
    override_data.get("include_tags")
    if "include_tags" in override_data
    else base_config.include_tags
  )
  exclude_tags_raw = (
    override_data.get("exclude_tags")
    if "exclude_tags" in override_data
    else base_config.exclude_tags
  )
  return TargetSettings(
    ops_per_interval=_parse_int_override(
      override_data.get("ops_per_interval"), base_config.ops_per_interval
    ),
    interval_s=_parse_int_override(override_data.get("interval_s"), base_config.interval_s),
    item_revisit_s=_parse_int_override(
      override_data.get("item_revisit_s"), base_config.item_revisit_s
    ),
    require_monitored=_parse_bool_override(
      override_data.get("require_monitored"), base_config.require_monitored
    ),
    require_cutoff_unmet=_parse_bool_override(
      override_data.get("require_cutoff_unmet"), base_config.require_cutoff_unmet
    ),
    released_only=_parse_bool_override(
      override_data.get("released_only"), base_config.released_only
    ),
    search_backoff_s=_parse_int_override(
      override_data.get("search_backoff_s"), base_config.search_backoff_s
    ),
    dry_run=_parse_bool_override(override_data.get("dry_run"), base_config.dry_run),
    include_tags=coerce_tag_set(include_tags_raw),
    exclude_tags=coerce_tag_set(exclude_tags_raw),
    min_missing_episodes=_parse_int_override(
      override_data.get("min_missing_episodes"), base_config.min_missing_episodes
    ),
    min_missing_percent=_parse_float_override(
      override_data.get("min_missing_percent"), base_config.min_missing_percent
    ),
  )


class ArrType(StrEnum):
  """Supported *arr service types."""

  RADARR = "radarr"
  SONARR = "sonarr"


class ArrTarget(BaseModel):
  """Configuration for a single *arr instance."""

  name: str
  arr_type: ArrType
  base_url: str
  api_key: str
  settings: TargetSettings
  _logging_ids: dict[str, str] | None = None

  @field_validator("name")
  @classmethod
  def validate_name(cls, v: str) -> str:
    """Validate name is non-empty."""
    if not v or not v.strip():
      raise ValueError("name must be non-empty")
    return v

  @field_validator("api_key")
  @classmethod
  def validate_api_key(cls, v: str) -> str:
    """Validate api_key is non-empty."""
    if not v or not v.strip():
      raise ValueError("api_key must be non-empty")
    return v

  @field_validator("base_url")
  @classmethod
  def validate_base_url(cls, v: str) -> str:
    """Validate base_url is a valid HTTP/HTTPS URL."""
    parsed = urlparse(v)
    if not parsed.scheme or not parsed.netloc:
      raise ValueError(f"base_url must be a valid URL, got: {v}")
    if parsed.scheme not in ("http", "https"):
      raise ValueError(f"base_url must use http or https scheme, got: {parsed.scheme}")
    return v

  def logging_ids(self) -> dict[str, str]:
    """Return logging identifiers for the target."""
    if self._logging_ids is None:
      self._logging_ids = {"target_name": self.name, "target_type": self.arr_type.value}
    return self._logging_ids

  def config_logging_tags(self) -> dict[str, int | float | bool | list[str]]:
    """Return target configuration values suitable for logging."""
    tags = self.model_dump(mode="json", exclude={"api_key", "settings"})
    settings_attrs = [
      ("ops_per_interval", lambda v: v),
      ("interval_s", lambda v: v),
      ("item_revisit_s", lambda v: v),
      ("require_monitored", lambda v: v),
      ("require_cutoff_unmet", lambda v: v),
      ("released_only", lambda v: v),
      ("search_backoff_s", lambda v: v),
      ("dry_run", lambda v: v),
      ("include_tags", lambda v: sorted(v)),
      ("exclude_tags", lambda v: sorted(v)),
      ("min_missing_episodes", lambda v: v),
      ("min_missing_percent", lambda v: v),
    ]

    for attr, transformer in settings_attrs:
      tags[attr] = transformer(getattr(self.settings, attr))
    return tags


class Config(BaseSettings):
  """Application configuration."""

  model_config = SettingsConfigDict(
    env_prefix="GTH_",
    case_sensitive=False,
    extra="ignore",
  )

  log_level: str = "INFO"
  metrics_enabled: bool = True
  metrics_address: str = "0.0.0.0"
  metrics_port: int = Field(default=9090, ge=1)
  state_file_path: str | None = "/data/state.yaml"
  ops_per_interval: int = Field(default=1, ge=1)
  interval_s: int = Field(default=60, ge=1)
  item_revisit_s: int = Field(default=604800, ge=1)
  require_monitored: bool = True
  require_cutoff_unmet: bool = True
  released_only: bool = False
  search_backoff_s: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: str = ""
  exclude_tags: str = ""
  min_missing_episodes: int = Field(default=0, ge=0)
  min_missing_percent: float = Field(default=0.0, ge=0.0, le=100.0)
  shutdown_timeout_s: float = Field(default=30.0, ge=0.0)
  targets: list[ArrTarget] = Field(default_factory=list, exclude=True)

  @field_validator("log_level")
  @classmethod
  def validate_log_level(cls, v: str) -> str:
    """Validate and normalize log level using logging module."""
    if not v or not v.strip():
      raise ValueError("log_level must be non-empty")
    level_upper = v.upper().strip()
    if level_upper == "WARN":
      level_upper = "WARNING"
    numeric_level = getattr(logging, level_upper, None)
    if numeric_level is not None and isinstance(numeric_level, int):
      result = logging.getLevelName(numeric_level)
      return str(result)
    result = logging.getLevelName(logging.INFO)
    return str(result)

  @field_validator("metrics_address")
  @classmethod
  def validate_metrics_address(cls, v: str) -> str:
    """Validate metrics_address is a valid IP address or hostname."""
    if not v or not v.strip():
      raise ValueError("metrics_address must be non-empty")
    address = v.strip()

    # Try parsing as IP address first
    try:
      ipaddress.ip_address(address)
      return address
    except ValueError:
      pass

    # Validate as hostname (RFC 1123)
    # Hostname can contain letters, digits, hyphens, and dots
    # Must start and end with alphanumeric character
    # Each label can be up to 63 characters
    hostname_pattern = re.compile(
      r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
    )
    if hostname_pattern.match(address):
      return address

    raise ValueError(f"metrics_address must be a valid IP address or hostname, got: {address}")

  @field_validator("state_file_path")
  @classmethod
  def validate_state_file_path(cls, v: str | None) -> str | None:
    """Validate state_file_path is writable, or None to skip validation."""
    if v is None:
      return None
    if not v or not v.strip():
      # Convert empty strings to None to skip validation
      return None
    path = Path(v.strip())

    # Check if the file exists and is writable
    if path.exists():
      if not os.access(path, os.W_OK):
        raise ValueError(f"state_file_path is not writable: {v}")
      return str(path)

    # File doesn't exist, check if parent directory exists and is writable
    parent = path.parent
    if not parent.exists():
      raise ValueError(f"state_file_path parent directory does not exist: {parent}")

    if not os.access(parent, os.W_OK):
      raise ValueError(f"state_file_path parent directory is not writable: {parent}")

    return str(path)


def _config_env_keys() -> frozenset[str]:
  """Env var names that Config reads (derived from model fields)."""
  return frozenset(f"GTH_{name.upper()}" for name in Config.model_fields if name != "targets")


def load_config(env: dict[str, str] | None = None) -> Config:
  """Load configuration from environment variables."""
  env_dict = dict(os.environ) if env is None else env
  if env is not None:
    os.environ.update(env)

  # Collect GTH_* keys and mark as used as we parse; fail if any remain unused.
  unused_gth_keys: set[str] = {k.upper() for k in env_dict if k.upper().startswith("GTH_")}
  unused_gth_keys -= _config_env_keys()

  base_config = Config()

  targets: list[ArrTarget] = []
  n = 0
  while True:
    type_key = f"GTH_ARR_{n}_TYPE"
    if type_key not in env_dict:
      break

    name_key = f"GTH_ARR_{n}_NAME"
    if name_key not in env_dict:
      raise ValueError(f"Missing required config: {name_key}")

    baseurl_key = f"GTH_ARR_{n}_BASEURL"
    if baseurl_key not in env_dict:
      raise ValueError(f"Missing required config: {baseurl_key}")

    apikey_key = f"GTH_ARR_{n}_APIKEY"
    if apikey_key not in env_dict:
      raise ValueError(f"Missing required config: {apikey_key}")

    # Mark target keys as used
    for key in (type_key, name_key, baseurl_key, apikey_key):
      unused_gth_keys.discard(key.upper())
    for env_suffix, _ in _TARGET_OVERRIDE_ENV_MAP:
      key = f"GTH_ARR_{n}_{env_suffix}"
      if key in env_dict:
        unused_gth_keys.discard(key.upper())

    try:
      arr_type = ArrType(env_dict[type_key].lower())
    except ValueError as e:
      allowed_types = "', '".join(member.value for member in ArrType)
      raise ValueError(
        f"Invalid arr type: {env_dict[type_key]}. Must be one of: '{allowed_types}'"
      ) from e

    override_data = _collect_target_override_data(env_dict, n)
    resolved_settings = _build_target_settings(base_config, override_data)

    target = ArrTarget(
      name=env_dict[name_key],
      arr_type=arr_type,
      base_url=env_dict[baseurl_key],
      api_key=env_dict[apikey_key],
      settings=resolved_settings,
    )
    logger.debug(
      "Target configuration created",
      index=n,
      **target.config_logging_tags(),
    )
    targets.append(target)
    n += 1

  if not targets:
    raise ValueError("At least one *arr target must be configured (GTH_ARR_0_*)")

  if unused_gth_keys:
    # Preserve original case from env for error message
    gth_key_to_original: dict[str, str] = {
      k.upper(): k for k in env_dict if k.upper().startswith("GTH_")
    }
    unrecognized = sorted(gth_key_to_original.get(k, k) for k in unused_gth_keys)
    raise ValueError(
      f"Unrecognized GTH_* environment variables: {', '.join(unrecognized)}. "
      "Check configuration for typos or consult the documentation."
    )

  config = Config()
  config.targets = targets
  logger.debug("Configuration loaded successfully", target_count=len(config.targets), config=config)
  return config
