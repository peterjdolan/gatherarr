from enum import Enum


class QualitySource(str, Enum):
  BLURAY = "bluray"
  BLURAYRAW = "blurayRaw"
  DVD = "dvd"
  TELEVISION = "television"
  TELEVISIONRAW = "televisionRaw"
  UNKNOWN = "unknown"
  WEB = "web"
  WEBRIP = "webRip"

  def __str__(self) -> str:
    return str(self.value)
