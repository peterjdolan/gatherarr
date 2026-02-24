"""Configuration loading and validation from environment variables."""

import ipaddress
import logging
import os
import re
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class TargetOverrideSettings(BaseSettings):
  """Temporary settings for parsing target-specific overrides."""

  model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

  ops_per_interval: int | None = Field(default=None, ge=1)
  interval_s: int | None = Field(default=None, ge=1)
  item_revisit_timeout_s: int | None = Field(default=None, ge=1)


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

    overrides = (
      TargetOverrideSettings.model_validate(override_data)
      if override_data
      else TargetOverrideSettings()
    )

    targets.append(
      ArrTarget(
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
      )
    )
    n += 1

  if not targets:
    raise ValueError("At least one *arr target must be configured (GTH_ARR_0_*)")

  config = Config()
  config.targets = targets
  return config
