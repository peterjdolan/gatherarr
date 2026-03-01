from enum import Enum


class SeriesStatusType(str, Enum):
  CONTINUING = "continuing"
  DELETED = "deleted"
  ENDED = "ended"
  UPCOMING = "upcoming"

  def __str__(self) -> str:
    return str(self.value)
