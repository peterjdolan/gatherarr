from enum import Enum


class RuntimeMode(str, Enum):
  CONSOLE = "console"
  SERVICE = "service"
  TRAY = "tray"

  def __str__(self) -> str:
    return str(self.value)
