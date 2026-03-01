from enum import Enum


class RejectionType(str, Enum):
  PERMANENT = "permanent"
  TEMPORARY = "temporary"

  def __str__(self) -> str:
    return str(self.value)
