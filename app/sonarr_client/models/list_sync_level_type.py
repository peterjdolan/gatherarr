from enum import Enum


class ListSyncLevelType(str, Enum):
  DISABLED = "disabled"
  KEEPANDTAG = "keepAndTag"
  KEEPANDUNMONITOR = "keepAndUnmonitor"
  LOGONLY = "logOnly"

  def __str__(self) -> str:
    return str(self.value)
