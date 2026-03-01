from enum import Enum


class UpdateMechanism(str, Enum):
  APT = "apt"
  BUILTIN = "builtIn"
  DOCKER = "docker"
  EXTERNAL = "external"
  SCRIPT = "script"

  def __str__(self) -> str:
    return str(self.value)
