from enum import Enum


class QueueStatus(str, Enum):
  COMPLETED = "completed"
  DELAY = "delay"
  DOWNLOADCLIENTUNAVAILABLE = "downloadClientUnavailable"
  DOWNLOADING = "downloading"
  FAILED = "failed"
  FALLBACK = "fallback"
  PAUSED = "paused"
  QUEUED = "queued"
  UNKNOWN = "unknown"
  WARNING = "warning"

  def __str__(self) -> str:
    return str(self.value)
