from enum import Enum


class TMDbCountryCode(str, Enum):
  AU = "au"
  BR = "br"
  CA = "ca"
  DE = "de"
  ES = "es"
  FR = "fr"
  GB = "gb"
  IE = "ie"
  IN = "in"
  IT = "it"
  NZ = "nz"
  RO = "ro"
  US = "us"

  def __str__(self) -> str:
    return str(self.value)
