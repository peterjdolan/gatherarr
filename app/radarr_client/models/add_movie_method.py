from enum import Enum


class AddMovieMethod(str, Enum):
  COLLECTION = "collection"
  LIST = "list"
  MANUAL = "manual"

  def __str__(self) -> str:
    return str(self.value)
