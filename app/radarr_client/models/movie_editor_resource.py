from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MovieEditorResource")


@_attrs_define
class MovieEditorResource:
  """
  Attributes:
      movie_ids (list[int] | None | Unset):
      monitored (bool | None | Unset):
      quality_profile_id (int | None | Unset):
      minimum_availability (MovieStatusType | Unset):
      root_folder_path (None | str | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      move_files (bool | Unset):
      delete_files (bool | Unset):
      add_import_exclusion (bool | Unset):
  """

  movie_ids: list[int] | None | Unset = UNSET
  monitored: bool | None | Unset = UNSET
  quality_profile_id: int | None | Unset = UNSET
  minimum_availability: MovieStatusType | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  move_files: bool | Unset = UNSET
  delete_files: bool | Unset = UNSET
  add_import_exclusion: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    movie_ids: list[int] | None | Unset
    if isinstance(self.movie_ids, Unset):
      movie_ids = UNSET
    elif isinstance(self.movie_ids, list):
      movie_ids = self.movie_ids

    else:
      movie_ids = self.movie_ids

    monitored: bool | None | Unset
    if isinstance(self.monitored, Unset):
      monitored = UNSET
    else:
      monitored = self.monitored

    quality_profile_id: int | None | Unset
    if isinstance(self.quality_profile_id, Unset):
      quality_profile_id = UNSET
    else:
      quality_profile_id = self.quality_profile_id

    minimum_availability: str | Unset = UNSET
    if not isinstance(self.minimum_availability, Unset):
      minimum_availability = self.minimum_availability.value

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

    add_import_exclusion = self.add_import_exclusion

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if movie_ids is not UNSET:
      field_dict["movieIds"] = movie_ids
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if minimum_availability is not UNSET:
      field_dict["minimumAvailability"] = minimum_availability
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
    if add_import_exclusion is not UNSET:
      field_dict["addImportExclusion"] = add_import_exclusion

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_movie_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        movie_ids_type_0 = cast(list[int], data)

        return movie_ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    movie_ids = _parse_movie_ids(d.pop("movieIds", UNSET))

    def _parse_monitored(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    monitored = _parse_monitored(d.pop("monitored", UNSET))

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

    add_import_exclusion = d.pop("addImportExclusion", UNSET)

    movie_editor_resource = cls(
      movie_ids=movie_ids,
      monitored=monitored,
      quality_profile_id=quality_profile_id,
      minimum_availability=minimum_availability,
      root_folder_path=root_folder_path,
      tags=tags,
      apply_tags=apply_tags,
      move_files=move_files,
      delete_files=delete_files,
      add_import_exclusion=add_import_exclusion,
    )

    return movie_editor_resource
