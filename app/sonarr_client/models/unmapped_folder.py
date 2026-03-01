from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnmappedFolder")


@_attrs_define
class UnmappedFolder:
  """
  Attributes:
      name (None | str | Unset):
      path (None | str | Unset):
      relative_path (None | str | Unset):
  """

  name: None | str | Unset = UNSET
  path: None | str | Unset = UNSET
  relative_path: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    relative_path: None | str | Unset
    if isinstance(self.relative_path, Unset):
      relative_path = UNSET
    else:
      relative_path = self.relative_path

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if name is not UNSET:
      field_dict["name"] = name
    if path is not UNSET:
      field_dict["path"] = path
    if relative_path is not UNSET:
      field_dict["relativePath"] = relative_path

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    def _parse_relative_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    relative_path = _parse_relative_path(d.pop("relativePath", UNSET))

    unmapped_folder = cls(
      name=name,
      path=path,
      relative_path=relative_path,
    )

    return unmapped_folder
