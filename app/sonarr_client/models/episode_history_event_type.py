from enum import Enum


class EpisodeHistoryEventType(str, Enum):
  DOWNLOADFAILED = "downloadFailed"
  DOWNLOADFOLDERIMPORTED = "downloadFolderImported"
  DOWNLOADIGNORED = "downloadIgnored"
  EPISODEFILEDELETED = "episodeFileDeleted"
  EPISODEFILERENAMED = "episodeFileRenamed"
  GRABBED = "grabbed"
  SERIESFOLDERIMPORTED = "seriesFolderImported"
  UNKNOWN = "unknown"

  def __str__(self) -> str:
    return str(self.value)
