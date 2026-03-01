from enum import Enum


class MovieStatusType(str, Enum):
  ANNOUNCED = "announced"
  DELETED = "deleted"
  INCINEMAS = "inCinemas"
  RELEASED = "released"
  TBA = "tba"

  def __str__(self) -> str:
    return str(self.value)
