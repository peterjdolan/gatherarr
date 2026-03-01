from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpUri")


@_attrs_define
class HttpUri:
  """
  Attributes:
      full_uri (None | str | Unset):
      scheme (None | str | Unset):
      host (None | str | Unset):
      port (int | None | Unset):
      path (None | str | Unset):
      query (None | str | Unset):
      fragment (None | str | Unset):
  """

  full_uri: None | str | Unset = UNSET
  scheme: None | str | Unset = UNSET
  host: None | str | Unset = UNSET
  port: int | None | Unset = UNSET
  path: None | str | Unset = UNSET
  query: None | str | Unset = UNSET
  fragment: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    full_uri: None | str | Unset
    if isinstance(self.full_uri, Unset):
      full_uri = UNSET
    else:
      full_uri = self.full_uri

    scheme: None | str | Unset
    if isinstance(self.scheme, Unset):
      scheme = UNSET
    else:
      scheme = self.scheme

    host: None | str | Unset
    if isinstance(self.host, Unset):
      host = UNSET
    else:
      host = self.host

    port: int | None | Unset
    if isinstance(self.port, Unset):
      port = UNSET
    else:
      port = self.port

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    query: None | str | Unset
    if isinstance(self.query, Unset):
      query = UNSET
    else:
      query = self.query

    fragment: None | str | Unset
    if isinstance(self.fragment, Unset):
      fragment = UNSET
    else:
      fragment = self.fragment

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if full_uri is not UNSET:
      field_dict["fullUri"] = full_uri
    if scheme is not UNSET:
      field_dict["scheme"] = scheme
    if host is not UNSET:
      field_dict["host"] = host
    if port is not UNSET:
      field_dict["port"] = port
    if path is not UNSET:
      field_dict["path"] = path
    if query is not UNSET:
      field_dict["query"] = query
    if fragment is not UNSET:
      field_dict["fragment"] = fragment

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_full_uri(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    full_uri = _parse_full_uri(d.pop("fullUri", UNSET))

    def _parse_scheme(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    scheme = _parse_scheme(d.pop("scheme", UNSET))

    def _parse_host(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    host = _parse_host(d.pop("host", UNSET))

    def _parse_port(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    port = _parse_port(d.pop("port", UNSET))

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    def _parse_query(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    query = _parse_query(d.pop("query", UNSET))

    def _parse_fragment(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    fragment = _parse_fragment(d.pop("fragment", UNSET))

    http_uri = cls(
      full_uri=full_uri,
      scheme=scheme,
      host=host,
      port=port,
      path=path,
      query=query,
      fragment=fragment,
    )

    return http_uri
