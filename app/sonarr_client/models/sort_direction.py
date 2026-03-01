from enum import Enum


class SortDirection(str, Enum):
  ASCENDING = "ascending"
  DEFAULT = "default"
  DESCENDING = "descending"

  def __str__(self) -> str:
    return str(self.value)
