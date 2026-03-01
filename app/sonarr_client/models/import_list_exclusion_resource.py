from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportListExclusionResource")


@_attrs_define
class ImportListExclusionResource:
  """
  Attributes:
      id (int | Unset):
      tvdb_id (int | Unset):
      title (None | str | Unset):
  """

  id: int | Unset = UNSET
  tvdb_id: int | Unset = UNSET
  title: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    tvdb_id = self.tvdb_id

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if tvdb_id is not UNSET:
      field_dict["tvdbId"] = tvdb_id
    if title is not UNSET:
      field_dict["title"] = title

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    tvdb_id = d.pop("tvdbId", UNSET)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    import_list_exclusion_resource = cls(
      id=id,
      tvdb_id=tvdb_id,
      title=title,
    )

    return import_list_exclusion_resource
