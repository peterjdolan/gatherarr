"""Structured logging redaction helpers."""

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

REDACTED_VALUE = "[REDACTED]"
SENSITIVE_KEYS = frozenset(
  {
    "api_key",
    "apikey",
    "x-api-key",
    "x_api_key",
  }
)


def redact_sensitive_fields(
  logger: Any, method_name: str, event_dict: Mapping[str, Any]
) -> dict[str, Any]:
  """Redact sensitive fields from structlog event dictionaries."""
  _ = logger
  _ = method_name
  return _redact_mapping(event_dict)


def _redact_value(value: Any) -> Any:
  """Redact sensitive keys recursively in supported container types."""
  if isinstance(value, dict):
    return _redact_mapping(value)
  if isinstance(value, list):
    return [_redact_value(item) for item in value]
  if isinstance(value, tuple):
    return tuple(_redact_value(item) for item in value)
  if hasattr(value, "model_dump"):
    return _redact_value(value.model_dump())
  if is_dataclass(value) and not isinstance(value, type):
    return _redact_value(asdict(value))
  return value


def _redact_mapping(mapping: Mapping[Any, Any]) -> dict[str, Any]:
  """Redact sensitive keys from a dictionary-like mapping."""
  redacted: dict[str, Any] = {}
  for key, value in mapping.items():
    key_str = str(key)
    if _is_sensitive_key(key_str):
      redacted[key_str] = REDACTED_VALUE
      continue
    redacted[key_str] = _redact_value(value)
  return redacted


def _is_sensitive_key(key: str) -> bool:
  """Return True when a key should be redacted."""
  return key.lower() in SENSITIVE_KEYS
