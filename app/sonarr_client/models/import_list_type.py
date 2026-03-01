from enum import Enum


class ImportListType(str, Enum):
  ADVANCED = "advanced"
  OTHER = "other"
  PLEX = "plex"
  PROGRAM = "program"
  SIMKL = "simkl"
  TRAKT = "trakt"

  def __str__(self) -> str:
    return str(self.value)
