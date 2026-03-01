from enum import Enum


class MediaCoverTypes(str, Enum):
  BANNER = "banner"
  CLEARLOGO = "clearlogo"
  FANART = "fanart"
  HEADSHOT = "headshot"
  POSTER = "poster"
  SCREENSHOT = "screenshot"
  UNKNOWN = "unknown"

  def __str__(self) -> str:
    return str(self.value)
