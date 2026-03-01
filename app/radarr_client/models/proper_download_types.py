from enum import Enum


class ProperDownloadTypes(str, Enum):
  DONOTPREFER = "doNotPrefer"
  DONOTUPGRADE = "doNotUpgrade"
  PREFERANDUPGRADE = "preferAndUpgrade"

  def __str__(self) -> str:
    return str(self.value)
