from enum import Enum


class CommandTrigger(str, Enum):
  MANUAL = "manual"
  SCHEDULED = "scheduled"
  UNSPECIFIED = "unspecified"

  def __str__(self) -> str:
    return str(self.value)
