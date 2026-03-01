from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskSpaceResource")


@_attrs_define
class DiskSpaceResource:
  """
  Attributes:
      id (int | Unset):
      path (None | str | Unset):
      label (None | str | Unset):
      free_space (int | Unset):
      total_space (int | Unset):
  """

  id: int | Unset = UNSET
  path: None | str | Unset = UNSET
  label: None | str | Unset = UNSET
  free_space: int | Unset = UNSET
  total_space: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    label: None | str | Unset
    if isinstance(self.label, Unset):
      label = UNSET
    else:
      label = self.label

    free_space = self.free_space

    total_space = self.total_space

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if path is not UNSET:
      field_dict["path"] = path
    if label is not UNSET:
      field_dict["label"] = label
    if free_space is not UNSET:
      field_dict["freeSpace"] = free_space
    if total_space is not UNSET:
      field_dict["totalSpace"] = total_space

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    def _parse_label(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    label = _parse_label(d.pop("label", UNSET))

    free_space = d.pop("freeSpace", UNSET)

    total_space = d.pop("totalSpace", UNSET)

    disk_space_resource = cls(
      id=id,
      path=path,
      label=label,
      free_space=free_space,
      total_space=total_space,
    )

    return disk_space_resource
