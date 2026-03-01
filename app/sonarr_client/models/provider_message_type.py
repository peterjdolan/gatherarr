from enum import Enum


class ProviderMessageType(str, Enum):
  ERROR = "error"
  INFO = "info"
  WARNING = "warning"

  def __str__(self) -> str:
    return str(self.value)
