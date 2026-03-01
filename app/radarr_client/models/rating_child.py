from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.rating_type import RatingType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RatingChild")


@_attrs_define
class RatingChild:
  """
  Attributes:
      votes (int | Unset):
      value (float | Unset):
      type_ (RatingType | Unset):
  """

  votes: int | Unset = UNSET
  value: float | Unset = UNSET
  type_: RatingType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    votes = self.votes

    value = self.value

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if votes is not UNSET:
      field_dict["votes"] = votes
    if value is not UNSET:
      field_dict["value"] = value
    if type_ is not UNSET:
      field_dict["type"] = type_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    votes = d.pop("votes", UNSET)

    value = d.pop("value", UNSET)

    _type_ = d.pop("type", UNSET)
    type_: RatingType | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = RatingType(_type_)

    rating_child = cls(
      votes=votes,
      value=value,
      type_=type_,
    )

    return rating_child
