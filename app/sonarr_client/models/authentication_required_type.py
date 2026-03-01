from enum import Enum


class AuthenticationRequiredType(str, Enum):
  DISABLEDFORLOCALADDRESSES = "disabledForLocalAddresses"
  ENABLED = "enabled"

  def __str__(self) -> str:
    return str(self.value)
