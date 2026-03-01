from enum import Enum


class ProxyType(str, Enum):
  HTTP = "http"
  SOCKS4 = "socks4"
  SOCKS5 = "socks5"

  def __str__(self) -> str:
    return str(self.value)
