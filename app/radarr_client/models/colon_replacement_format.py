from enum import Enum


class ColonReplacementFormat(str, Enum):
  DASH = "dash"
  DELETE = "delete"
  SMART = "smart"
  SPACEDASH = "spaceDash"
  SPACEDASHSPACE = "spaceDashSpace"

  def __str__(self) -> str:
    return str(self.value)
