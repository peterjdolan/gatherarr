from enum import Enum


class FileDateType(str, Enum):
  CINEMAS = "cinemas"
  NONE = "none"
  RELEASE = "release"

  def __str__(self) -> str:
    return str(self.value)
