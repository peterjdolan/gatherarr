from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.release_type import ReleaseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.language import Language
  from ..models.media_info_resource import MediaInfoResource
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="EpisodeFileResource")


@_attrs_define
class EpisodeFileResource:
  """
  Attributes:
      id (int | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      relative_path (None | str | Unset):
      path (None | str | Unset):
      size (int | Unset):
      date_added (datetime.datetime | Unset):
      scene_name (None | str | Unset):
      release_group (None | str | Unset):
      languages (list[Language] | None | Unset):
      quality (QualityModel | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      custom_format_score (int | Unset):
      indexer_flags (int | None | Unset):
      release_type (ReleaseType | Unset):
      media_info (MediaInfoResource | Unset):
      quality_cutoff_not_met (bool | Unset):
  """

  id: int | Unset = UNSET
  series_id: int | Unset = UNSET
  season_number: int | Unset = UNSET
  relative_path: None | str | Unset = UNSET
  path: None | str | Unset = UNSET
  size: int | Unset = UNSET
  date_added: datetime.datetime | Unset = UNSET
  scene_name: None | str | Unset = UNSET
  release_group: None | str | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  custom_format_score: int | Unset = UNSET
  indexer_flags: int | None | Unset = UNSET
  release_type: ReleaseType | Unset = UNSET
  media_info: MediaInfoResource | Unset = UNSET
  quality_cutoff_not_met: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    series_id = self.series_id

    season_number = self.season_number

    relative_path: None | str | Unset
    if isinstance(self.relative_path, Unset):
      relative_path = UNSET
    else:
      relative_path = self.relative_path

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    size = self.size

    date_added: str | Unset = UNSET
    if not isinstance(self.date_added, Unset):
      date_added = self.date_added.isoformat()

    scene_name: None | str | Unset
    if isinstance(self.scene_name, Unset):
      scene_name = UNSET
    else:
      scene_name = self.scene_name

    release_group: None | str | Unset
    if isinstance(self.release_group, Unset):
      release_group = UNSET
    else:
      release_group = self.release_group

    languages: list[dict[str, Any]] | None | Unset
    if isinstance(self.languages, Unset):
      languages = UNSET
    elif isinstance(self.languages, list):
      languages = []
      for languages_type_0_item_data in self.languages:
        languages_type_0_item = languages_type_0_item_data.to_dict()
        languages.append(languages_type_0_item)

    else:
      languages = self.languages

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    custom_formats: list[dict[str, Any]] | None | Unset
    if isinstance(self.custom_formats, Unset):
      custom_formats = UNSET
    elif isinstance(self.custom_formats, list):
      custom_formats = []
      for custom_formats_type_0_item_data in self.custom_formats:
        custom_formats_type_0_item = custom_formats_type_0_item_data.to_dict()
        custom_formats.append(custom_formats_type_0_item)

    else:
      custom_formats = self.custom_formats

    custom_format_score = self.custom_format_score

    indexer_flags: int | None | Unset
    if isinstance(self.indexer_flags, Unset):
      indexer_flags = UNSET
    else:
      indexer_flags = self.indexer_flags

    release_type: str | Unset = UNSET
    if not isinstance(self.release_type, Unset):
      release_type = self.release_type.value

    media_info: dict[str, Any] | Unset = UNSET
    if not isinstance(self.media_info, Unset):
      media_info = self.media_info.to_dict()

    quality_cutoff_not_met = self.quality_cutoff_not_met

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if series_id is not UNSET:
      field_dict["seriesId"] = series_id
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if relative_path is not UNSET:
      field_dict["relativePath"] = relative_path
    if path is not UNSET:
      field_dict["path"] = path
    if size is not UNSET:
      field_dict["size"] = size
    if date_added is not UNSET:
      field_dict["dateAdded"] = date_added
    if scene_name is not UNSET:
      field_dict["sceneName"] = scene_name
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group
    if languages is not UNSET:
      field_dict["languages"] = languages
    if quality is not UNSET:
      field_dict["quality"] = quality
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if custom_format_score is not UNSET:
      field_dict["customFormatScore"] = custom_format_score
    if indexer_flags is not UNSET:
      field_dict["indexerFlags"] = indexer_flags
    if release_type is not UNSET:
      field_dict["releaseType"] = release_type
    if media_info is not UNSET:
      field_dict["mediaInfo"] = media_info
    if quality_cutoff_not_met is not UNSET:
      field_dict["qualityCutoffNotMet"] = quality_cutoff_not_met

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.language import Language
    from ..models.media_info_resource import MediaInfoResource
    from ..models.quality_model import QualityModel

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    series_id = d.pop("seriesId", UNSET)

    season_number = d.pop("seasonNumber", UNSET)

    def _parse_relative_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    relative_path = _parse_relative_path(d.pop("relativePath", UNSET))

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    size = d.pop("size", UNSET)

    _date_added = d.pop("dateAdded", UNSET)
    date_added: datetime.datetime | Unset
    if isinstance(_date_added, Unset):
      date_added = UNSET
    else:
      date_added = isoparse(_date_added)

    def _parse_scene_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    scene_name = _parse_scene_name(d.pop("sceneName", UNSET))

    def _parse_release_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_group = _parse_release_group(d.pop("releaseGroup", UNSET))

    def _parse_languages(data: object) -> list[Language] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        languages_type_0 = []
        _languages_type_0 = data
        for languages_type_0_item_data in _languages_type_0:
          languages_type_0_item = Language.from_dict(languages_type_0_item_data)

          languages_type_0.append(languages_type_0_item)

        return languages_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[Language] | None | Unset, data)

    languages = _parse_languages(d.pop("languages", UNSET))

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

    def _parse_custom_formats(data: object) -> list[CustomFormatResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        custom_formats_type_0 = []
        _custom_formats_type_0 = data
        for custom_formats_type_0_item_data in _custom_formats_type_0:
          custom_formats_type_0_item = CustomFormatResource.from_dict(
            custom_formats_type_0_item_data
          )

          custom_formats_type_0.append(custom_formats_type_0_item)

        return custom_formats_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[CustomFormatResource] | None | Unset, data)

    custom_formats = _parse_custom_formats(d.pop("customFormats", UNSET))

    custom_format_score = d.pop("customFormatScore", UNSET)

    def _parse_indexer_flags(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    indexer_flags = _parse_indexer_flags(d.pop("indexerFlags", UNSET))

    _release_type = d.pop("releaseType", UNSET)
    release_type: ReleaseType | Unset
    if isinstance(_release_type, Unset):
      release_type = UNSET
    else:
      release_type = ReleaseType(_release_type)

    _media_info = d.pop("mediaInfo", UNSET)
    media_info: MediaInfoResource | Unset
    if isinstance(_media_info, Unset):
      media_info = UNSET
    else:
      media_info = MediaInfoResource.from_dict(_media_info)

    quality_cutoff_not_met = d.pop("qualityCutoffNotMet", UNSET)

    episode_file_resource = cls(
      id=id,
      series_id=series_id,
      season_number=season_number,
      relative_path=relative_path,
      path=path,
      size=size,
      date_added=date_added,
      scene_name=scene_name,
      release_group=release_group,
      languages=languages,
      quality=quality,
      custom_formats=custom_formats,
      custom_format_score=custom_format_score,
      indexer_flags=indexer_flags,
      release_type=release_type,
      media_info=media_info,
      quality_cutoff_not_met=quality_cutoff_not_met,
    )

    return episode_file_resource
