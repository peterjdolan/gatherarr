from enum import Enum


class HealthCheckResult(str, Enum):
  ERROR = "error"
  NOTICE = "notice"
  OK = "ok"
  WARNING = "warning"

  def __str__(self) -> str:
    return str(self.value)
