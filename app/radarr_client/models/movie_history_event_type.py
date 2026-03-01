from enum import Enum


class MovieHistoryEventType(str, Enum):
  DOWNLOADFAILED = "downloadFailed"
  DOWNLOADFOLDERIMPORTED = "downloadFolderImported"
  DOWNLOADIGNORED = "downloadIgnored"
  GRABBED = "grabbed"
  MOVIEFILEDELETED = "movieFileDeleted"
  MOVIEFILERENAMED = "movieFileRenamed"
  MOVIEFOLDERIMPORTED = "movieFolderImported"
  UNKNOWN = "unknown"

  def __str__(self) -> str:
    return str(self.value)
