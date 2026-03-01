from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.list_sync_level_type import ListSyncLevelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportListConfigResource")


@_attrs_define
class ImportListConfigResource:
  """
  Attributes:
      id (int | Unset):
      list_sync_level (ListSyncLevelType | Unset):
      list_sync_tag (int | Unset):
  """

  id: int | Unset = UNSET
  list_sync_level: ListSyncLevelType | Unset = UNSET
  list_sync_tag: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    list_sync_level: str | Unset = UNSET
    if not isinstance(self.list_sync_level, Unset):
      list_sync_level = self.list_sync_level.value

    list_sync_tag = self.list_sync_tag

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if list_sync_level is not UNSET:
      field_dict["listSyncLevel"] = list_sync_level
    if list_sync_tag is not UNSET:
      field_dict["listSyncTag"] = list_sync_tag

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    _list_sync_level = d.pop("listSyncLevel", UNSET)
    list_sync_level: ListSyncLevelType | Unset
    if isinstance(_list_sync_level, Unset):
      list_sync_level = UNSET
    else:
      list_sync_level = ListSyncLevelType(_list_sync_level)

    list_sync_tag = d.pop("listSyncTag", UNSET)

    import_list_config_resource = cls(
      id=id,
      list_sync_level=list_sync_level,
      list_sync_tag=list_sync_tag,
    )

    return import_list_config_resource
