from enum import Enum


class QualitySource(str, Enum):
  BLURAY = "bluray"
  CAM = "cam"
  DVD = "dvd"
  TELECINE = "telecine"
  TELESYNC = "telesync"
  TV = "tv"
  UNKNOWN = "unknown"
  WEBDL = "webdl"
  WEBRIP = "webrip"
  WORKPRINT = "workprint"

  def __str__(self) -> str:
    return str(self.value)
