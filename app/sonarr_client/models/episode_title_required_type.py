from enum import Enum


class EpisodeTitleRequiredType(str, Enum):
  ALWAYS = "always"
  BULKSEASONRELEASES = "bulkSeasonReleases"
  NEVER = "never"

  def __str__(self) -> str:
    return str(self.value)
