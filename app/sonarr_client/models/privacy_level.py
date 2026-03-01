from enum import Enum


class PrivacyLevel(str, Enum):
  APIKEY = "apiKey"
  NORMAL = "normal"
  PASSWORD = "password"
  USERNAME = "userName"

  def __str__(self) -> str:
    return str(self.value)
