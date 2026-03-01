from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFormatBulkResource")


@_attrs_define
class CustomFormatBulkResource:
  """
  Attributes:
      ids (list[int] | None | Unset):
      include_custom_format_when_renaming (bool | None | Unset):
  """

  ids: list[int] | None | Unset = UNSET
  include_custom_format_when_renaming: bool | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    ids: list[int] | None | Unset
    if isinstance(self.ids, Unset):
      ids = UNSET
    elif isinstance(self.ids, list):
      ids = self.ids

    else:
      ids = self.ids

    include_custom_format_when_renaming: bool | None | Unset
    if isinstance(self.include_custom_format_when_renaming, Unset):
      include_custom_format_when_renaming = UNSET
    else:
      include_custom_format_when_renaming = self.include_custom_format_when_renaming

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if ids is not UNSET:
      field_dict["ids"] = ids
    if include_custom_format_when_renaming is not UNSET:
      field_dict["includeCustomFormatWhenRenaming"] = include_custom_format_when_renaming

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        ids_type_0 = cast(list[int], data)

        return ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    ids = _parse_ids(d.pop("ids", UNSET))

    def _parse_include_custom_format_when_renaming(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    include_custom_format_when_renaming = _parse_include_custom_format_when_renaming(
      d.pop("includeCustomFormatWhenRenaming", UNSET)
    )

    custom_format_bulk_resource = cls(
      ids=ids,
      include_custom_format_when_renaming=include_custom_format_when_renaming,
    )

    return custom_format_bulk_resource
