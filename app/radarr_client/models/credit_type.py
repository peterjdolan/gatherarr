from enum import Enum


class CreditType(str, Enum):
  CAST = "cast"
  CREW = "crew"

  def __str__(self) -> str:
    return str(self.value)
