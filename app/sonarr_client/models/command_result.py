from enum import Enum


class CommandResult(str, Enum):
  SUCCESSFUL = "successful"
  UNKNOWN = "unknown"
  UNSUCCESSFUL = "unsuccessful"

  def __str__(self) -> str:
    return str(self.value)
