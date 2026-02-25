"""Tests for structured log redaction."""

from dataclasses import dataclass
from typing import Any

from app.config import ArrTarget, ArrType
from app.log_redaction import REDACTED_VALUE, redact_sensitive_fields


@dataclass
class Credentials:
  """Test credentials dataclass for redaction checks."""

  name: str
  api_key: str


class TestLogRedaction:
  def test_redacts_sensitive_keys_recursively(self) -> None:
    """Redaction should apply to nested dictionaries and lists."""
    event_dict: dict[str, Any] = {
      "api_key": "root-secret",
      "payload": {
        "apikey": "nested-secret",
        "headers": {
          "X-Api-Key": "header-secret",
          "other": "safe",
        },
      },
      "items": [
        {"x_api_key": "list-secret"},
        {"value": "safe-value"},
      ],
    }

    redacted = redact_sensitive_fields(logger=object(), method_name="debug", event_dict=event_dict)

    assert redacted["api_key"] == REDACTED_VALUE
    assert redacted["payload"]["apikey"] == REDACTED_VALUE
    assert redacted["payload"]["headers"]["X-Api-Key"] == REDACTED_VALUE
    assert redacted["payload"]["headers"]["other"] == "safe"
    assert redacted["items"][0]["x_api_key"] == REDACTED_VALUE
    assert redacted["items"][1]["value"] == "safe-value"

  def test_redacts_sensitive_fields_in_pydantic_models(self) -> None:
    """Redaction should sanitize pydantic model fields named api_key."""
    target = ArrTarget(
      name="Test Target",
      arr_type=ArrType.RADARR,
      base_url="http://radarr:7878",
      api_key="model-secret",
      ops_per_interval=1,
      interval_s=60,
      item_revisit_timeout_s=86400,
    )

    redacted = redact_sensitive_fields(
      logger=object(),
      method_name="debug",
      event_dict={"target": target},
    )

    assert redacted["target"]["api_key"] == REDACTED_VALUE
    assert redacted["target"]["name"] == "Test Target"

  def test_redacts_sensitive_fields_in_dataclasses(self) -> None:
    """Redaction should sanitize dataclass fields named api_key."""
    credentials = Credentials(name="service-account", api_key="dataclass-secret")
    redacted = redact_sensitive_fields(
      logger=object(),
      method_name="info",
      event_dict={"credentials": credentials},
    )

    assert redacted["credentials"]["api_key"] == REDACTED_VALUE
    assert redacted["credentials"]["name"] == "service-account"
