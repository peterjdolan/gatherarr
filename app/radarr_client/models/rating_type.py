from enum import Enum


class RatingType(str, Enum):
  CRITIC = "critic"
  USER = "user"

  def __str__(self) -> str:
    return str(self.value)
