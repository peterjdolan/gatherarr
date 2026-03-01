from enum import Enum


class CalendarReleaseType(str, Enum):
  CINEMARELEASE = "cinemaRelease"
  DIGITALRELEASE = "digitalRelease"
  PHYSICALRELEASE = "physicalRelease"

  def __str__(self) -> str:
    return str(self.value)
