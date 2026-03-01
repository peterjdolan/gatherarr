from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemotePathMappingResource")


@_attrs_define
class RemotePathMappingResource:
  """
  Attributes:
      id (int | Unset):
      host (None | str | Unset):
      remote_path (None | str | Unset):
      local_path (None | str | Unset):
  """

  id: int | Unset = UNSET
  host: None | str | Unset = UNSET
  remote_path: None | str | Unset = UNSET
  local_path: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    host: None | str | Unset
    if isinstance(self.host, Unset):
      host = UNSET
    else:
      host = self.host

    remote_path: None | str | Unset
    if isinstance(self.remote_path, Unset):
      remote_path = UNSET
    else:
      remote_path = self.remote_path

    local_path: None | str | Unset
    if isinstance(self.local_path, Unset):
      local_path = UNSET
    else:
      local_path = self.local_path

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if host is not UNSET:
      field_dict["host"] = host
    if remote_path is not UNSET:
      field_dict["remotePath"] = remote_path
    if local_path is not UNSET:
      field_dict["localPath"] = local_path

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_host(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    host = _parse_host(d.pop("host", UNSET))

    def _parse_remote_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    remote_path = _parse_remote_path(d.pop("remotePath", UNSET))

    def _parse_local_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    local_path = _parse_local_path(d.pop("localPath", UNSET))

    remote_path_mapping_resource = cls(
      id=id,
      host=host,
      remote_path=remote_path,
      local_path=local_path,
    )

    return remote_path_mapping_resource
