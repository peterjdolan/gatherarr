from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Language")


@_attrs_define
class Language:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name

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

    language = cls(
      id=id,
      name=name,
    )

    return language
