from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="QualityDefinitionLimitsResource")


@_attrs_define
class QualityDefinitionLimitsResource:
  """
  Attributes:
      min_ (int | Unset):
      max_ (int | Unset):
  """

  min_: int | Unset = UNSET
  max_: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    min_ = self.min_

    max_ = self.max_

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if min_ is not UNSET:
      field_dict["min"] = min_
    if max_ is not UNSET:
      field_dict["max"] = max_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    min_ = d.pop("min", UNSET)

    max_ = d.pop("max", UNSET)

    quality_definition_limits_resource = cls(
      min_=min_,
      max_=max_,
    )

    return quality_definition_limits_resource
