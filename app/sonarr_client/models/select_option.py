from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SelectOption")


@_attrs_define
class SelectOption:
  """
  Attributes:
      value (int | Unset):
      name (None | str | Unset):
      order (int | Unset):
      hint (None | str | Unset):
  """

  value: int | Unset = UNSET
  name: None | str | Unset = UNSET
  order: int | Unset = UNSET
  hint: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    value = self.value

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    order = self.order

    hint: None | str | Unset
    if isinstance(self.hint, Unset):
      hint = UNSET
    else:
      hint = self.hint

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if value is not UNSET:
      field_dict["value"] = value
    if name is not UNSET:
      field_dict["name"] = name
    if order is not UNSET:
      field_dict["order"] = order
    if hint is not UNSET:
      field_dict["hint"] = hint

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    value = d.pop("value", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    order = d.pop("order", UNSET)

    def _parse_hint(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    hint = _parse_hint(d.pop("hint", UNSET))

    select_option = cls(
      value=value,
      name=name,
      order=order,
      hint=hint,
    )

    return select_option
