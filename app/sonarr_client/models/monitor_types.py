from enum import Enum


class MonitorTypes(str, Enum):
  ALL = "all"
  EXISTING = "existing"
  FIRSTSEASON = "firstSeason"
  FUTURE = "future"
  LASTSEASON = "lastSeason"
  LATESTSEASON = "latestSeason"
  MISSING = "missing"
  MONITORSPECIALS = "monitorSpecials"
  NONE = "none"
  PILOT = "pilot"
  RECENT = "recent"
  SKIP = "skip"
  UNKNOWN = "unknown"
  UNMONITORSPECIALS = "unmonitorSpecials"

  def __str__(self) -> str:
    return str(self.value)
