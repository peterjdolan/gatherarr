"""Configuration loading and validation from environment variables."""

import ipaddress
import logging
import os
import re
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlparse

import structlog
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger()


def _parse_csv_tags(value: str) -> list[str]:
  """Parse comma-separated tags into a normalized list."""
  tags: list[str] = []
  seen: set[str] = set()
  for raw_tag in value.split(","):
    normalized_tag = raw_tag.strip()
    if not normalized_tag:
      continue
    if normalized_tag in seen:
      continue
    seen.add(normalized_tag)
    tags.append(normalized_tag)
  return tags


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
  max_searches_per_item_per_day: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: list[str] = Field(default_factory=list)
  exclude_tags: list[str] = Field(default_factory=list)
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
  def normalize_tags(cls, v: object) -> list[str]:
    """Normalize include/exclude tags from CSV string or list."""
    if isinstance(v, str):
      return _parse_csv_tags(v)
    if isinstance(v, list):
      normalized_tags: list[str] = []
      seen: set[str] = set()
      for raw_tag in v:
        normalized_tag = str(raw_tag).strip()
        if not normalized_tag:
          continue
        if normalized_tag in seen:
          continue
        seen.add(normalized_tag)
        normalized_tags.append(normalized_tag)
      return normalized_tags
    if v is None:
      return []
    raise ValueError("include_tags and exclude_tags must be a CSV string or list")

  def logging_ids(self) -> dict[str, str]:
    """Return logging identifiers for the target."""
    if self._logging_ids is None:
      self._logging_ids = {"target_name": self.name, "target_type": self.arr_type.value}
    return self._logging_ids


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
  max_searches_per_item_per_day: int | None = Field(default=None, ge=0)
  dry_run: bool | None = None
  include_tags: str | None = None
  exclude_tags: str | None = None
  min_missing_episodes: int | None = Field(default=None, ge=0)
  min_missing_percent: float | None = Field(default=None, ge=0.0, le=100.0)


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
  max_searches_per_item_per_day: int = Field(default=0, ge=0)
  dry_run: bool = False
  include_tags: str = ""
  exclude_tags: str = ""
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

    override_data: dict[str, str] = {}
    if f"GTH_ARR_{n}_OPS_PER_INTERVAL" in env_dict:
      override_data["ops_per_interval"] = env_dict[f"GTH_ARR_{n}_OPS_PER_INTERVAL"]
    if f"GTH_ARR_{n}_INTERVAL_S" in env_dict:
      override_data["interval_s"] = env_dict[f"GTH_ARR_{n}_INTERVAL_S"]
    if f"GTH_ARR_{n}_ITEM_REVISIT_TIMEOUT_S" in env_dict:
      override_data["item_revisit_timeout_s"] = env_dict[f"GTH_ARR_{n}_ITEM_REVISIT_TIMEOUT_S"]
    if f"GTH_ARR_{n}_REQUIRE_MONITORED" in env_dict:
      override_data["require_monitored"] = env_dict[f"GTH_ARR_{n}_REQUIRE_MONITORED"]
    if f"GTH_ARR_{n}_REQUIRE_CUTOFF_UNMET" in env_dict:
      override_data["require_cutoff_unmet"] = env_dict[f"GTH_ARR_{n}_REQUIRE_CUTOFF_UNMET"]
    if f"GTH_ARR_{n}_RELEASED_ONLY" in env_dict:
      override_data["released_only"] = env_dict[f"GTH_ARR_{n}_RELEASED_ONLY"]
    if f"GTH_ARR_{n}_SEARCH_BACKOFF_S" in env_dict:
      override_data["search_backoff_s"] = env_dict[f"GTH_ARR_{n}_SEARCH_BACKOFF_S"]
    if f"GTH_ARR_{n}_MAX_SEARCHES_PER_ITEM_PER_DAY" in env_dict:
      override_data["max_searches_per_item_per_day"] = env_dict[
        f"GTH_ARR_{n}_MAX_SEARCHES_PER_ITEM_PER_DAY"
      ]
    if f"GTH_ARR_{n}_DRY_RUN" in env_dict:
      override_data["dry_run"] = env_dict[f"GTH_ARR_{n}_DRY_RUN"]
    if f"GTH_ARR_{n}_INCLUDE_TAGS" in env_dict:
      override_data["include_tags"] = env_dict[f"GTH_ARR_{n}_INCLUDE_TAGS"]
    if f"GTH_ARR_{n}_EXCLUDE_TAGS" in env_dict:
      override_data["exclude_tags"] = env_dict[f"GTH_ARR_{n}_EXCLUDE_TAGS"]
    if f"GTH_ARR_{n}_MIN_MISSING_EPISODES" in env_dict:
      override_data["min_missing_episodes"] = env_dict[f"GTH_ARR_{n}_MIN_MISSING_EPISODES"]
    if f"GTH_ARR_{n}_MIN_MISSING_PERCENT" in env_dict:
      override_data["min_missing_percent"] = env_dict[f"GTH_ARR_{n}_MIN_MISSING_PERCENT"]

    overrides = (
      TargetOverrideSettings.model_validate(override_data)
      if override_data
      else TargetOverrideSettings()
    )

    target = ArrTarget(
      name=env_dict[name_key],
      arr_type=arr_type,
      base_url=env_dict[baseurl_key],
      api_key=env_dict[apikey_key],
      ops_per_interval=overrides.ops_per_interval
      if overrides.ops_per_interval is not None
      else base_config.ops_per_interval,
      interval_s=overrides.interval_s
      if overrides.interval_s is not None
      else base_config.interval_s,
      item_revisit_timeout_s=overrides.item_revisit_timeout_s
      if overrides.item_revisit_timeout_s is not None
      else base_config.item_revisit_s,
      require_monitored=overrides.require_monitored
      if overrides.require_monitored is not None
      else base_config.require_monitored,
      require_cutoff_unmet=overrides.require_cutoff_unmet
      if overrides.require_cutoff_unmet is not None
      else base_config.require_cutoff_unmet,
      released_only=overrides.released_only
      if overrides.released_only is not None
      else base_config.released_only,
      search_backoff_s=overrides.search_backoff_s
      if overrides.search_backoff_s is not None
      else base_config.search_backoff_s,
      max_searches_per_item_per_day=overrides.max_searches_per_item_per_day
      if overrides.max_searches_per_item_per_day is not None
      else base_config.max_searches_per_item_per_day,
      dry_run=overrides.dry_run if overrides.dry_run is not None else base_config.dry_run,
      include_tags=_parse_csv_tags(overrides.include_tags)
      if overrides.include_tags is not None
      else _parse_csv_tags(base_config.include_tags),
      exclude_tags=_parse_csv_tags(overrides.exclude_tags)
      if overrides.exclude_tags is not None
      else _parse_csv_tags(base_config.exclude_tags),
      min_missing_episodes=overrides.min_missing_episodes
      if overrides.min_missing_episodes is not None
      else base_config.min_missing_episodes,
      min_missing_percent=overrides.min_missing_percent
      if overrides.min_missing_percent is not None
      else base_config.min_missing_percent,
    )
    logger.debug(
      "Target configuration created",
      index=n,
      name=target.name,
      arr_type=target.arr_type.value,
      base_url=target.base_url,
      ops_per_interval=target.ops_per_interval,
      interval_s=target.interval_s,
      item_revisit_timeout_s=target.item_revisit_timeout_s,
      require_monitored=target.require_monitored,
      require_cutoff_unmet=target.require_cutoff_unmet,
      released_only=target.released_only,
      search_backoff_s=target.search_backoff_s,
      max_searches_per_item_per_day=target.max_searches_per_item_per_day,
      dry_run=target.dry_run,
      include_tags=target.include_tags,
      exclude_tags=target.exclude_tags,
      min_missing_episodes=target.min_missing_episodes,
      min_missing_percent=target.min_missing_percent,
    )
    targets.append(target)
    n += 1

  if not targets:
    raise ValueError("At least one *arr target must be configured (GTH_ARR_0_*)")

  config = Config()
  config.targets = targets
  logger.debug("Configuration loaded successfully", target_count=len(config.targets), config=config)
  return config
