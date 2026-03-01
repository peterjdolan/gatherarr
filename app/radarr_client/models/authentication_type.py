from enum import Enum


class AuthenticationType(str, Enum):
  BASIC = "basic"
  EXTERNAL = "external"
  FORMS = "forms"
  NONE = "none"

  def __str__(self) -> str:
    return str(self.value)
