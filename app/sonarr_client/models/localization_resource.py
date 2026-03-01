from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.localization_resource_strings_type_0 import LocalizationResourceStringsType0


T = TypeVar("T", bound="LocalizationResource")


@_attrs_define
class LocalizationResource:
  """
  Attributes:
      id (int | Unset):
      strings (LocalizationResourceStringsType0 | None | Unset):
  """

  id: int | Unset = UNSET
  strings: LocalizationResourceStringsType0 | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    from ..models.localization_resource_strings_type_0 import LocalizationResourceStringsType0

    id = self.id

    strings: dict[str, Any] | None | Unset
    if isinstance(self.strings, Unset):
      strings = UNSET
    elif isinstance(self.strings, LocalizationResourceStringsType0):
      strings = self.strings.to_dict()
    else:
      strings = self.strings

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if strings is not UNSET:
      field_dict["strings"] = strings

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.localization_resource_strings_type_0 import LocalizationResourceStringsType0

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_strings(data: object) -> LocalizationResourceStringsType0 | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, dict):
          raise TypeError()
        strings_type_0 = LocalizationResourceStringsType0.from_dict(data)

        return strings_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(LocalizationResourceStringsType0 | None | Unset, data)

    strings = _parse_strings(d.pop("strings", UNSET))

    localization_resource = cls(
      id=id,
      strings=strings,
    )

    return localization_resource
