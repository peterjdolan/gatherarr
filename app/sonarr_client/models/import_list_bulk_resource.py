from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportListBulkResource")


@_attrs_define
class ImportListBulkResource:
  """
  Attributes:
      ids (list[int] | None | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      enable_automatic_add (bool | None | Unset):
      root_folder_path (None | str | Unset):
      quality_profile_id (int | None | Unset):
  """

  ids: list[int] | None | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  enable_automatic_add: bool | None | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  quality_profile_id: int | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    ids: list[int] | None | Unset
    if isinstance(self.ids, Unset):
      ids = UNSET
    elif isinstance(self.ids, list):
      ids = self.ids

    else:
      ids = self.ids

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    apply_tags: str | Unset = UNSET
    if not isinstance(self.apply_tags, Unset):
      apply_tags = self.apply_tags.value

    enable_automatic_add: bool | None | Unset
    if isinstance(self.enable_automatic_add, Unset):
      enable_automatic_add = UNSET
    else:
      enable_automatic_add = self.enable_automatic_add

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

    quality_profile_id: int | None | Unset
    if isinstance(self.quality_profile_id, Unset):
      quality_profile_id = UNSET
    else:
      quality_profile_id = self.quality_profile_id

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if ids is not UNSET:
      field_dict["ids"] = ids
    if tags is not UNSET:
      field_dict["tags"] = tags
    if apply_tags is not UNSET:
      field_dict["applyTags"] = apply_tags
    if enable_automatic_add is not UNSET:
      field_dict["enableAutomaticAdd"] = enable_automatic_add
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id

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

    def _parse_tags(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        tags_type_0 = cast(list[int], data)

        return tags_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    tags = _parse_tags(d.pop("tags", UNSET))

    _apply_tags = d.pop("applyTags", UNSET)
    apply_tags: ApplyTags | Unset
    if isinstance(_apply_tags, Unset):
      apply_tags = UNSET
    else:
      apply_tags = ApplyTags(_apply_tags)

    def _parse_enable_automatic_add(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable_automatic_add = _parse_enable_automatic_add(d.pop("enableAutomaticAdd", UNSET))

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

    def _parse_quality_profile_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    quality_profile_id = _parse_quality_profile_id(d.pop("qualityProfileId", UNSET))

    import_list_bulk_resource = cls(
      ids=ids,
      tags=tags,
      apply_tags=apply_tags,
      enable_automatic_add=enable_automatic_add,
      root_folder_path=root_folder_path,
      quality_profile_id=quality_profile_id,
    )

    return import_list_bulk_resource
