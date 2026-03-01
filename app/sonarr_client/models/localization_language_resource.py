from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocalizationLanguageResource")


@_attrs_define
class LocalizationLanguageResource:
  """
  Attributes:
      identifier (None | str | Unset):
  """

  identifier: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    identifier: None | str | Unset
    if isinstance(self.identifier, Unset):
      identifier = UNSET
    else:
      identifier = self.identifier

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if identifier is not UNSET:
      field_dict["identifier"] = identifier

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_identifier(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    identifier = _parse_identifier(d.pop("identifier", UNSET))

    localization_language_resource = cls(
      identifier=identifier,
    )

    return localization_language_resource
