from enum import Enum


class BackupType(str, Enum):
  MANUAL = "manual"
  SCHEDULED = "scheduled"
  UPDATE = "update"

  def __str__(self) -> str:
    return str(self.value)
