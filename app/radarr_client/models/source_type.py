from enum import Enum


class SourceType(str, Enum):
  INDEXER = "indexer"
  MAPPINGS = "mappings"
  TMDB = "tmdb"
  USER = "user"

  def __str__(self) -> str:
    return str(self.value)
