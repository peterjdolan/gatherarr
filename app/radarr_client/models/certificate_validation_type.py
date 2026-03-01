from enum import Enum


class CertificateValidationType(str, Enum):
  DISABLED = "disabled"
  DISABLEDFORLOCALADDRESSES = "disabledForLocalAddresses"
  ENABLED = "enabled"

  def __str__(self) -> str:
    return str(self.value)
