from enum import Enum


class TrackedDownloadState(str, Enum):
  DOWNLOADING = "downloading"
  FAILED = "failed"
  FAILEDPENDING = "failedPending"
  IGNORED = "ignored"
  IMPORTBLOCKED = "importBlocked"
  IMPORTED = "imported"
  IMPORTING = "importing"
  IMPORTPENDING = "importPending"

  def __str__(self) -> str:
    return str(self.value)
