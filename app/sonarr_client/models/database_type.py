from enum import Enum


class DatabaseType(str, Enum):
  POSTGRESQL = "postgreSQL"
  SQLITE = "sqLite"

  def __str__(self) -> str:
    return str(self.value)
