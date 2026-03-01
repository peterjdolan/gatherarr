from enum import Enum


class MonitorTypes(str, Enum):
  MOVIEANDCOLLECTION = "movieAndCollection"
  MOVIEONLY = "movieOnly"
  NONE = "none"

  def __str__(self) -> str:
    return str(self.value)
