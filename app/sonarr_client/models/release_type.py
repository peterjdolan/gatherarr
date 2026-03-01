from enum import Enum


class ReleaseType(str, Enum):
  MULTIEPISODE = "multiEpisode"
  SEASONPACK = "seasonPack"
  SINGLEEPISODE = "singleEpisode"
  UNKNOWN = "unknown"

  def __str__(self) -> str:
    return str(self.value)
