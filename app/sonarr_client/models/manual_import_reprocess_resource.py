from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.release_type import ReleaseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.episode_resource import EpisodeResource
  from ..models.import_rejection_resource import ImportRejectionResource
  from ..models.language import Language
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="ManualImportReprocessResource")


@_attrs_define
class ManualImportReprocessResource:
  """
  Attributes:
      id (int | Unset):
      path (None | str | Unset):
      series_id (int | Unset):
      season_number (int | None | Unset):
      episodes (list[EpisodeResource] | None | Unset):
      episode_ids (list[int] | None | Unset):
      quality (QualityModel | Unset):
      languages (list[Language] | None | Unset):
      release_group (None | str | Unset):
      download_id (None | str | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      custom_format_score (int | Unset):
      indexer_flags (int | Unset):
      release_type (ReleaseType | Unset):
      rejections (list[ImportRejectionResource] | None | Unset):
  """

  id: int | Unset = UNSET
  path: None | str | Unset = UNSET
  series_id: int | Unset = UNSET
  season_number: int | None | Unset = UNSET
  episodes: list[EpisodeResource] | None | Unset = UNSET
  episode_ids: list[int] | None | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  release_group: None | str | Unset = UNSET
  download_id: None | str | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  custom_format_score: int | Unset = UNSET
  indexer_flags: int | Unset = UNSET
  release_type: ReleaseType | Unset = UNSET
  rejections: list[ImportRejectionResource] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    series_id = self.series_id

    season_number: int | None | Unset
    if isinstance(self.season_number, Unset):
      season_number = UNSET
    else:
      season_number = self.season_number

    episodes: list[dict[str, Any]] | None | Unset
    if isinstance(self.episodes, Unset):
      episodes = UNSET
    elif isinstance(self.episodes, list):
      episodes = []
      for episodes_type_0_item_data in self.episodes:
        episodes_type_0_item = episodes_type_0_item_data.to_dict()
        episodes.append(episodes_type_0_item)

    else:
      episodes = self.episodes

    episode_ids: list[int] | None | Unset
    if isinstance(self.episode_ids, Unset):
      episode_ids = UNSET
    elif isinstance(self.episode_ids, list):
      episode_ids = self.episode_ids

    else:
      episode_ids = self.episode_ids

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

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

    release_group: None | str | Unset
    if isinstance(self.release_group, Unset):
      release_group = UNSET
    else:
      release_group = self.release_group

    download_id: None | str | Unset
    if isinstance(self.download_id, Unset):
      download_id = UNSET
    else:
      download_id = self.download_id

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

    indexer_flags = self.indexer_flags

    release_type: str | Unset = UNSET
    if not isinstance(self.release_type, Unset):
      release_type = self.release_type.value

    rejections: list[dict[str, Any]] | None | Unset
    if isinstance(self.rejections, Unset):
      rejections = UNSET
    elif isinstance(self.rejections, list):
      rejections = []
      for rejections_type_0_item_data in self.rejections:
        rejections_type_0_item = rejections_type_0_item_data.to_dict()
        rejections.append(rejections_type_0_item)

    else:
      rejections = self.rejections

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if path is not UNSET:
      field_dict["path"] = path
    if series_id is not UNSET:
      field_dict["seriesId"] = series_id
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if episodes is not UNSET:
      field_dict["episodes"] = episodes
    if episode_ids is not UNSET:
      field_dict["episodeIds"] = episode_ids
    if quality is not UNSET:
      field_dict["quality"] = quality
    if languages is not UNSET:
      field_dict["languages"] = languages
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group
    if download_id is not UNSET:
      field_dict["downloadId"] = download_id
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if custom_format_score is not UNSET:
      field_dict["customFormatScore"] = custom_format_score
    if indexer_flags is not UNSET:
      field_dict["indexerFlags"] = indexer_flags
    if release_type is not UNSET:
      field_dict["releaseType"] = release_type
    if rejections is not UNSET:
      field_dict["rejections"] = rejections

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.episode_resource import EpisodeResource
    from ..models.import_rejection_resource import ImportRejectionResource
    from ..models.language import Language
    from ..models.quality_model import QualityModel

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    series_id = d.pop("seriesId", UNSET)

    def _parse_season_number(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    season_number = _parse_season_number(d.pop("seasonNumber", UNSET))

    def _parse_episodes(data: object) -> list[EpisodeResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        episodes_type_0 = []
        _episodes_type_0 = data
        for episodes_type_0_item_data in _episodes_type_0:
          episodes_type_0_item = EpisodeResource.from_dict(episodes_type_0_item_data)

          episodes_type_0.append(episodes_type_0_item)

        return episodes_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[EpisodeResource] | None | Unset, data)

    episodes = _parse_episodes(d.pop("episodes", UNSET))

    def _parse_episode_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        episode_ids_type_0 = cast(list[int], data)

        return episode_ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    episode_ids = _parse_episode_ids(d.pop("episodeIds", UNSET))

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

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

    def _parse_release_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_group = _parse_release_group(d.pop("releaseGroup", UNSET))

    def _parse_download_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_id = _parse_download_id(d.pop("downloadId", UNSET))

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

    indexer_flags = d.pop("indexerFlags", UNSET)

    _release_type = d.pop("releaseType", UNSET)
    release_type: ReleaseType | Unset
    if isinstance(_release_type, Unset):
      release_type = UNSET
    else:
      release_type = ReleaseType(_release_type)

    def _parse_rejections(data: object) -> list[ImportRejectionResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        rejections_type_0 = []
        _rejections_type_0 = data
        for rejections_type_0_item_data in _rejections_type_0:
          rejections_type_0_item = ImportRejectionResource.from_dict(rejections_type_0_item_data)

          rejections_type_0.append(rejections_type_0_item)

        return rejections_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[ImportRejectionResource] | None | Unset, data)

    rejections = _parse_rejections(d.pop("rejections", UNSET))

    manual_import_reprocess_resource = cls(
      id=id,
      path=path,
      series_id=series_id,
      season_number=season_number,
      episodes=episodes,
      episode_ids=episode_ids,
      quality=quality,
      languages=languages,
      release_group=release_group,
      download_id=download_id,
      custom_formats=custom_formats,
      custom_format_score=custom_format_score,
      indexer_flags=indexer_flags,
      release_type=release_type,
      rejections=rejections,
    )

    return manual_import_reprocess_resource
