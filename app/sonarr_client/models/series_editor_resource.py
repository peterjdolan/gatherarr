from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..models.new_item_monitor_types import NewItemMonitorTypes
from ..models.series_types import SeriesTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="SeriesEditorResource")


@_attrs_define
class SeriesEditorResource:
  """
  Attributes:
      series_ids (list[int] | None | Unset):
      monitored (bool | None | Unset):
      monitor_new_items (NewItemMonitorTypes | Unset):
      quality_profile_id (int | None | Unset):
      series_type (SeriesTypes | Unset):
      season_folder (bool | None | Unset):
      root_folder_path (None | str | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      move_files (bool | Unset):
      delete_files (bool | Unset):
      add_import_list_exclusion (bool | Unset):
  """

  series_ids: list[int] | None | Unset = UNSET
  monitored: bool | None | Unset = UNSET
  monitor_new_items: NewItemMonitorTypes | Unset = UNSET
  quality_profile_id: int | None | Unset = UNSET
  series_type: SeriesTypes | Unset = UNSET
  season_folder: bool | None | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  move_files: bool | Unset = UNSET
  delete_files: bool | Unset = UNSET
  add_import_list_exclusion: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    series_ids: list[int] | None | Unset
    if isinstance(self.series_ids, Unset):
      series_ids = UNSET
    elif isinstance(self.series_ids, list):
      series_ids = self.series_ids

    else:
      series_ids = self.series_ids

    monitored: bool | None | Unset
    if isinstance(self.monitored, Unset):
      monitored = UNSET
    else:
      monitored = self.monitored

    monitor_new_items: str | Unset = UNSET
    if not isinstance(self.monitor_new_items, Unset):
      monitor_new_items = self.monitor_new_items.value

    quality_profile_id: int | None | Unset
    if isinstance(self.quality_profile_id, Unset):
      quality_profile_id = UNSET
    else:
      quality_profile_id = self.quality_profile_id

    series_type: str | Unset = UNSET
    if not isinstance(self.series_type, Unset):
      series_type = self.series_type.value

    season_folder: bool | None | Unset
    if isinstance(self.season_folder, Unset):
      season_folder = UNSET
    else:
      season_folder = self.season_folder

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

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

    move_files = self.move_files

    delete_files = self.delete_files

    add_import_list_exclusion = self.add_import_list_exclusion

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if series_ids is not UNSET:
      field_dict["seriesIds"] = series_ids
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if monitor_new_items is not UNSET:
      field_dict["monitorNewItems"] = monitor_new_items
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if series_type is not UNSET:
      field_dict["seriesType"] = series_type
    if season_folder is not UNSET:
      field_dict["seasonFolder"] = season_folder
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if tags is not UNSET:
      field_dict["tags"] = tags
    if apply_tags is not UNSET:
      field_dict["applyTags"] = apply_tags
    if move_files is not UNSET:
      field_dict["moveFiles"] = move_files
    if delete_files is not UNSET:
      field_dict["deleteFiles"] = delete_files
    if add_import_list_exclusion is not UNSET:
      field_dict["addImportListExclusion"] = add_import_list_exclusion

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_series_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        series_ids_type_0 = cast(list[int], data)

        return series_ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    series_ids = _parse_series_ids(d.pop("seriesIds", UNSET))

    def _parse_monitored(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    monitored = _parse_monitored(d.pop("monitored", UNSET))

    _monitor_new_items = d.pop("monitorNewItems", UNSET)
    monitor_new_items: NewItemMonitorTypes | Unset
    if isinstance(_monitor_new_items, Unset):
      monitor_new_items = UNSET
    else:
      monitor_new_items = NewItemMonitorTypes(_monitor_new_items)

    def _parse_quality_profile_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    quality_profile_id = _parse_quality_profile_id(d.pop("qualityProfileId", UNSET))

    _series_type = d.pop("seriesType", UNSET)
    series_type: SeriesTypes | Unset
    if isinstance(_series_type, Unset):
      series_type = UNSET
    else:
      series_type = SeriesTypes(_series_type)

    def _parse_season_folder(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    season_folder = _parse_season_folder(d.pop("seasonFolder", UNSET))

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

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

    move_files = d.pop("moveFiles", UNSET)

    delete_files = d.pop("deleteFiles", UNSET)

    add_import_list_exclusion = d.pop("addImportListExclusion", UNSET)

    series_editor_resource = cls(
      series_ids=series_ids,
      monitored=monitored,
      monitor_new_items=monitor_new_items,
      quality_profile_id=quality_profile_id,
      series_type=series_type,
      season_folder=season_folder,
      root_folder_path=root_folder_path,
      tags=tags,
      apply_tags=apply_tags,
      move_files=move_files,
      delete_files=delete_files,
      add_import_list_exclusion=add_import_list_exclusion,
    )

    return series_editor_resource
