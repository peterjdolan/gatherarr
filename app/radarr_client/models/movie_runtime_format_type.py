from enum import Enum


class MovieRuntimeFormatType(str, Enum):
  HOURSMINUTES = "hoursMinutes"
  MINUTES = "minutes"

  def __str__(self) -> str:
    return str(self.value)
