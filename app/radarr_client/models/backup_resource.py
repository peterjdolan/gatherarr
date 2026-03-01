from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.backup_type import BackupType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BackupResource")


@_attrs_define
class BackupResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      path (None | str | Unset):
      type_ (BackupType | Unset):
      size (int | Unset):
      time (datetime.datetime | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  path: None | str | Unset = UNSET
  type_: BackupType | Unset = UNSET
  size: int | Unset = UNSET
  time: datetime.datetime | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

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

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    size = self.size

    time: str | Unset = UNSET
    if not isinstance(self.time, Unset):
      time = self.time.isoformat()

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if path is not UNSET:
      field_dict["path"] = path
    if type_ is not UNSET:
      field_dict["type"] = type_
    if size is not UNSET:
      field_dict["size"] = size
    if time is not UNSET:
      field_dict["time"] = time

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

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

    _type_ = d.pop("type", UNSET)
    type_: BackupType | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = BackupType(_type_)

    size = d.pop("size", UNSET)

    _time = d.pop("time", UNSET)
    time: datetime.datetime | Unset
    if isinstance(_time, Unset):
      time = UNSET
    else:
      time = isoparse(_time)

    backup_resource = cls(
      id=id,
      name=name,
      path=path,
      type_=type_,
      size=size,
      time=time,
    )

    return backup_resource
