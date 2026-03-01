from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileFormatItemResource")


@_attrs_define
class ProfileFormatItemResource:
  """
  Attributes:
      id (int | Unset):
      format_ (int | Unset):
      name (None | str | Unset):
      score (int | Unset):
  """

  id: int | Unset = UNSET
  format_: int | Unset = UNSET
  name: None | str | Unset = UNSET
  score: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    format_ = self.format_

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    score = self.score

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if format_ is not UNSET:
      field_dict["format"] = format_
    if name is not UNSET:
      field_dict["name"] = name
    if score is not UNSET:
      field_dict["score"] = score

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    format_ = d.pop("format", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    score = d.pop("score", UNSET)

    profile_format_item_resource = cls(
      id=id,
      format_=format_,
      name=name,
      score=score,
    )

    return profile_format_item_resource
