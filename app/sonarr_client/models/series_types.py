from enum import Enum


class SeriesTypes(str, Enum):
  ANIME = "anime"
  DAILY = "daily"
  STANDARD = "standard"

  def __str__(self) -> str:
    return str(self.value)
