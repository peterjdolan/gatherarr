"""A client library for accessing Sonarr"""

from .client import AuthenticatedClient, Client

__all__ = (
  "AuthenticatedClient",
  "Client",
)
