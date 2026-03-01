from enum import Enum


class CommandStatus(str, Enum):
  ABORTED = "aborted"
  CANCELLED = "cancelled"
  COMPLETED = "completed"
  FAILED = "failed"
  ORPHANED = "orphaned"
  QUEUED = "queued"
  STARTED = "started"

  def __str__(self) -> str:
    return str(self.value)
