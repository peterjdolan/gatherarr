from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.language import Language
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="EpisodeFileListResource")


@_attrs_define
class EpisodeFileListResource:
  """
  Attributes:
      episode_file_ids (list[int] | None | Unset):
      languages (list[Language] | None | Unset):
      quality (QualityModel | Unset):
      scene_name (None | str | Unset):
      release_group (None | str | Unset):
  """

  episode_file_ids: list[int] | None | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  scene_name: None | str | Unset = UNSET
  release_group: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    episode_file_ids: list[int] | None | Unset
    if isinstance(self.episode_file_ids, Unset):
      episode_file_ids = UNSET
    elif isinstance(self.episode_file_ids, list):
      episode_file_ids = self.episode_file_ids

    else:
      episode_file_ids = self.episode_file_ids

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

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if episode_file_ids is not UNSET:
      field_dict["episodeFileIds"] = episode_file_ids
    if languages is not UNSET:
      field_dict["languages"] = languages
    if quality is not UNSET:
      field_dict["quality"] = quality
    if scene_name is not UNSET:
      field_dict["sceneName"] = scene_name
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.language import Language
    from ..models.quality_model import QualityModel

    d = dict(src_dict)

    def _parse_episode_file_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        episode_file_ids_type_0 = cast(list[int], data)

        return episode_file_ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    episode_file_ids = _parse_episode_file_ids(d.pop("episodeFileIds", UNSET))

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

    episode_file_list_resource = cls(
      episode_file_ids=episode_file_ids,
      languages=languages,
      quality=quality,
      scene_name=scene_name,
      release_group=release_group,
    )

    return episode_file_list_resource
