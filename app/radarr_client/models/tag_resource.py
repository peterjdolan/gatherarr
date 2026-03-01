from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagResource")


@_attrs_define
class TagResource:
  """
  Attributes:
      id (int | Unset):
      label (None | str | Unset):
  """

  id: int | Unset = UNSET
  label: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    label: None | str | Unset
    if isinstance(self.label, Unset):
      label = UNSET
    else:
      label = self.label

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if label is not UNSET:
      field_dict["label"] = label

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_label(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    label = _parse_label(d.pop("label", UNSET))

    tag_resource = cls(
      id=id,
      label=label,
    )

    return tag_resource
