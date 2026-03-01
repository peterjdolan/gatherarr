from enum import Enum


class FileDateType(str, Enum):
  LOCALAIRDATE = "localAirDate"
  NONE = "none"
  UTCAIRDATE = "utcAirDate"

  def __str__(self) -> str:
    return str(self.value)
