from enum import Enum


class RescanAfterRefreshType(str, Enum):
  AFTERMANUAL = "afterManual"
  ALWAYS = "always"
  NEVER = "never"

  def __str__(self) -> str:
    return str(self.value)
