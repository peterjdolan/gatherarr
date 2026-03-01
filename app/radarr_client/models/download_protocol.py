from enum import Enum


class DownloadProtocol(str, Enum):
  TORRENT = "torrent"
  UNKNOWN = "unknown"
  USENET = "usenet"

  def __str__(self) -> str:
    return str(self.value)
