"""Configuration loading and validation from environment variables."""

import ipaddress
import logging
import os
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, TypeVar
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
  ("ITEM_REVISIT_TIMEOUT_S", "item_revisit_timeout_s"),
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


@dataclass(frozen=True)
class ResolvedTargetSettings:
  """Resolved settings for target-level behavior."""

  ops_per_interval: int
  interval_s: int
  item_revisit_timeout_s: int
  require_monitored: bool
  require_cutoff_unmet: bool
  released_only: bool
  search_backoff_s: int
  dry_run: bool
  include_tags: set[str]
  exclude_tags: set[str]
  min_missing_episodes: int
  min_missing_percent: float

  def to_dict(self) -> dict[str, Any]:
    """Serialize resolved settings for ArrTarget construction."""
    return {
      "ops_per_interval": self.ops_per_interval,
      "interval_s": self.interval_s,
      "item_revisit_timeout_s": self.item_revisit_timeout_s,
      "require_monitored": self.require_monitored,
      "require_cutoff_unmet": self.require_cutoff_unmet,
      "released_only": self.released_only,
      "search_backoff_s": self.search_backoff_s,
      "dry_run": self.dry_run,
      "include_tags": self.include_tags,
      "exclude_tags": self.exclude_tags,
      "min_missing_episodes": self.min_missing_episodes,
      "min_missing_percent": self.min_missing_percent,
    }


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


def _build_target_settings(
  base_config: "Config", overrides: "TargetOverrideSettings"
) -> ResolvedTargetSettings:
  """Build resolved target settings from defaults and per-target overrides."""
  include_tags_raw = _resolve_override_value(overrides.include_tags, base_config.include_tags)
  exclude_tags_raw = _resolve_override_value(overrides.exclude_tags, base_config.exclude_tags)
  return ResolvedTargetSettings(
    ops_per_interval=_resolve_override_value(
      overrides.ops_per_interval, base_config.ops_per_interval
    ),
    interval_s=_resolve_override_value(overrides.interval_s, base_config.interval_s),
    item_revisit_timeout_s=_resolve_override_value(
      overrides.item_revisit_timeout_s, base_config.item_revisit_s
    ),
    require_monitored=_resolve_override_value(
      overrides.require_monitored, base_config.require_monitored
    ),
    require_cutoff_unmet=_resolve_override_value(
      overrides.require_cutoff_unmet, base_config.require_cutoff_unmet
    ),
    released_only=_resolve_override_value(overrides.released_only, base_config.released_only),
    search_backoff_s=_resolve_override_value(
      overrides.search_backoff_s, base_config.search_backoff_s
    ),
    dry_run=_resolve_override_value(overrides.dry_run, base_config.dry_run),
    include_tags=coerce_tag_set(include_tags_raw),
    exclude_tags=coerce_tag_set(exclude_tags_raw),
    min_missing_episodes=_resolve_override_value(
      overrides.min_missing_episodes, base_config.min_missing_episodes
    ),
    min_missing_percent=_resolve_override_value(
      overrides.min_missing_percent, base_config.min_missing_percent
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
  ops_per_interval: int = Field(ge=1)
  interval_s: int = Field(ge=1)
  item_revisit_timeout_s: int = Field(ge=1)
  require_monitored: bool = True
  require_cutoff_unmet: bool = True
  released_only: bool = False
  search_backoff_s: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: set[str] = Field(default_factory=set)
  exclude_tags: set[str] = Field(default_factory=set)
  min_missing_episodes: int = Field(default=0, ge=0)
  min_missing_percent: float = Field(default=0.0, ge=0.0, le=100.0)
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

  @field_validator("include_tags", "exclude_tags", mode="before")
  @classmethod
  def normalize_tags(cls, v: object) -> set[str]:
    """Normalize include/exclude tags from CSV or iterable values."""
    return coerce_tag_set(v)

  def logging_ids(self) -> dict[str, str]:
    """Return logging identifiers for the target."""
    if self._logging_ids is None:
      self._logging_ids = {"target_name": self.name, "target_type": self.arr_type.value}
    return self._logging_ids

  def config_logging_tags(self) -> dict[str, Any]:
    """Return target configuration values suitable for logging."""
    tags = self.model_dump(mode="json", exclude={"api_key"})
    tags["include_tags"] = sorted(self.include_tags)
    tags["exclude_tags"] = sorted(self.exclude_tags)
    return tags


class TargetOverrideSettings(BaseSettings):
  """Temporary settings for parsing target-specific overrides."""

  model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

  ops_per_interval: int | None = Field(default=None, ge=1)
  interval_s: int | None = Field(default=None, ge=1)
  item_revisit_timeout_s: int | None = Field(default=None, ge=1)
  require_monitored: bool | None = None
  require_cutoff_unmet: bool | None = None
  released_only: bool | None = None
  search_backoff_s: int | None = Field(default=None, ge=0)
  dry_run: bool | None = None
  include_tags: set[str] | None = None
  exclude_tags: set[str] | None = None
  min_missing_episodes: int | None = Field(default=None, ge=0)
  min_missing_percent: float | None = Field(default=None, ge=0.0, le=100.0)

  @field_validator("include_tags", "exclude_tags", mode="before")
  @classmethod
  def normalize_optional_tags(cls, v: object) -> set[str] | None:
    """Normalize include/exclude tags to sets when overrides are present."""
    if v is None:
      return None
    return coerce_tag_set(v)


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
  item_revisit_s: int = Field(default=86400, ge=1)
  require_monitored: bool = True
  require_cutoff_unmet: bool = True
  released_only: bool = False
  search_backoff_s: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: set[str] = Field(default_factory=set)
  exclude_tags: set[str] = Field(default_factory=set)
  min_missing_episodes: int = Field(default=0, ge=0)
  min_missing_percent: float = Field(default=0.0, ge=0.0, le=100.0)
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

  @field_validator("include_tags", "exclude_tags", mode="before")
  @classmethod
  def normalize_global_tags(cls, v: object) -> set[str]:
    """Normalize global include/exclude tags."""
    return coerce_tag_set(v)

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


def load_config(env: dict[str, str] | None = None) -> Config:
  """Load configuration from environment variables."""
  env_dict = dict(os.environ) if env is None else env
  if env is not None:
    os.environ.update(env)

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

    try:
      arr_type = ArrType(env_dict[type_key].lower())
    except ValueError as e:
      allowed_types = "', '".join(member.value for member in ArrType)
      raise ValueError(
        f"Invalid arr type: {env_dict[type_key]}. Must be one of: '{allowed_types}'"
      ) from e

    override_data = _collect_target_override_data(env_dict, n)

    overrides = (
      TargetOverrideSettings.model_validate(override_data)
      if override_data
      else TargetOverrideSettings()
    )
    resolved_settings = _build_target_settings(base_config, overrides)

    target = ArrTarget(
      name=env_dict[name_key],
      arr_type=arr_type,
      base_url=env_dict[baseurl_key],
      api_key=env_dict[apikey_key],
      **resolved_settings.to_dict(),
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

  config = Config()
  config.targets = targets
  logger.debug("Configuration loaded successfully", target_count=len(config.targets), config=config)
  return config
