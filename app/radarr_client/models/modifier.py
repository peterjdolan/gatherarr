from enum import Enum


class Modifier(str, Enum):
  BRDISK = "brdisk"
  NONE = "none"
  RAWHD = "rawhd"
  REGIONAL = "regional"
  REMUX = "remux"
  SCREENER = "screener"

  def __str__(self) -> str:
    return str(self.value)
