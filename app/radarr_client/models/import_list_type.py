from enum import Enum


class ImportListType(str, Enum):
  ADVANCED = "advanced"
  OTHER = "other"
  PLEX = "plex"
  PROGRAM = "program"
  SIMKL = "simkl"
  TMDB = "tmdb"
  TRAKT = "trakt"

  def __str__(self) -> str:
    return str(self.value)
