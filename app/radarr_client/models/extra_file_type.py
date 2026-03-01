from enum import Enum


class ExtraFileType(str, Enum):
  METADATA = "metadata"
  OTHER = "other"
  SUBTITLE = "subtitle"

  def __str__(self) -> str:
    return str(self.value)
