from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportListBulkResource")


@_attrs_define
class ImportListBulkResource:
  """
  Attributes:
      ids (list[int] | None | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      enabled (bool | None | Unset):
      enable_auto (bool | None | Unset):
      root_folder_path (None | str | Unset):
      quality_profile_id (int | None | Unset):
      minimum_availability (MovieStatusType | Unset):
  """

  ids: list[int] | None | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  enabled: bool | None | Unset = UNSET
  enable_auto: bool | None | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  quality_profile_id: int | None | Unset = UNSET
  minimum_availability: MovieStatusType | Unset = UNSET

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

    enabled: bool | None | Unset
    if isinstance(self.enabled, Unset):
      enabled = UNSET
    else:
      enabled = self.enabled

    enable_auto: bool | None | Unset
    if isinstance(self.enable_auto, Unset):
      enable_auto = UNSET
    else:
      enable_auto = self.enable_auto

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

    minimum_availability: str | Unset = UNSET
    if not isinstance(self.minimum_availability, Unset):
      minimum_availability = self.minimum_availability.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if ids is not UNSET:
      field_dict["ids"] = ids
    if tags is not UNSET:
      field_dict["tags"] = tags
    if apply_tags is not UNSET:
      field_dict["applyTags"] = apply_tags
    if enabled is not UNSET:
      field_dict["enabled"] = enabled
    if enable_auto is not UNSET:
      field_dict["enableAuto"] = enable_auto
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if minimum_availability is not UNSET:
      field_dict["minimumAvailability"] = minimum_availability

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

    def _parse_enabled(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enabled = _parse_enabled(d.pop("enabled", UNSET))

    def _parse_enable_auto(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable_auto = _parse_enable_auto(d.pop("enableAuto", UNSET))

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

    _minimum_availability = d.pop("minimumAvailability", UNSET)
    minimum_availability: MovieStatusType | Unset
    if isinstance(_minimum_availability, Unset):
      minimum_availability = UNSET
    else:
      minimum_availability = MovieStatusType(_minimum_availability)

    import_list_bulk_resource = cls(
      ids=ids,
      tags=tags,
      apply_tags=apply_tags,
      enabled=enabled,
      enable_auto=enable_auto,
      root_folder_path=root_folder_path,
      quality_profile_id=quality_profile_id,
      minimum_availability=minimum_availability,
    )

    return import_list_bulk_resource
