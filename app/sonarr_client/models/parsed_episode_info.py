from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.release_type import ReleaseType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.language import Language
  from ..models.quality_model import QualityModel
  from ..models.series_title_info import SeriesTitleInfo


T = TypeVar("T", bound="ParsedEpisodeInfo")


@_attrs_define
class ParsedEpisodeInfo:
  """
  Attributes:
      release_title (None | str | Unset):
      series_title (None | str | Unset):
      series_title_info (SeriesTitleInfo | Unset):
      quality (QualityModel | Unset):
      season_number (int | Unset):
      episode_numbers (list[int] | None | Unset):
      absolute_episode_numbers (list[int] | None | Unset):
      special_absolute_episode_numbers (list[float] | None | Unset):
      air_date (None | str | Unset):
      languages (list[Language] | None | Unset):
      full_season (bool | Unset):
      is_partial_season (bool | Unset):
      is_multi_season (bool | Unset):
      is_season_extra (bool | Unset):
      is_split_episode (bool | Unset):
      is_mini_series (bool | Unset):
      special (bool | Unset):
      release_group (None | str | Unset):
      release_hash (None | str | Unset):
      season_part (int | Unset):
      release_tokens (None | str | Unset):
      daily_part (int | None | Unset):
      is_daily (bool | Unset):
      is_absolute_numbering (bool | Unset):
      is_possible_special_episode (bool | Unset):
      is_possible_scene_season_special (bool | Unset):
      release_type (ReleaseType | Unset):
  """

  release_title: None | str | Unset = UNSET
  series_title: None | str | Unset = UNSET
  series_title_info: SeriesTitleInfo | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  season_number: int | Unset = UNSET
  episode_numbers: list[int] | None | Unset = UNSET
  absolute_episode_numbers: list[int] | None | Unset = UNSET
  special_absolute_episode_numbers: list[float] | None | Unset = UNSET
  air_date: None | str | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  full_season: bool | Unset = UNSET
  is_partial_season: bool | Unset = UNSET
  is_multi_season: bool | Unset = UNSET
  is_season_extra: bool | Unset = UNSET
  is_split_episode: bool | Unset = UNSET
  is_mini_series: bool | Unset = UNSET
  special: bool | Unset = UNSET
  release_group: None | str | Unset = UNSET
  release_hash: None | str | Unset = UNSET
  season_part: int | Unset = UNSET
  release_tokens: None | str | Unset = UNSET
  daily_part: int | None | Unset = UNSET
  is_daily: bool | Unset = UNSET
  is_absolute_numbering: bool | Unset = UNSET
  is_possible_special_episode: bool | Unset = UNSET
  is_possible_scene_season_special: bool | Unset = UNSET
  release_type: ReleaseType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    release_title: None | str | Unset
    if isinstance(self.release_title, Unset):
      release_title = UNSET
    else:
      release_title = self.release_title

    series_title: None | str | Unset
    if isinstance(self.series_title, Unset):
      series_title = UNSET
    else:
      series_title = self.series_title

    series_title_info: dict[str, Any] | Unset = UNSET
    if not isinstance(self.series_title_info, Unset):
      series_title_info = self.series_title_info.to_dict()

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    season_number = self.season_number

    episode_numbers: list[int] | None | Unset
    if isinstance(self.episode_numbers, Unset):
      episode_numbers = UNSET
    elif isinstance(self.episode_numbers, list):
      episode_numbers = self.episode_numbers

    else:
      episode_numbers = self.episode_numbers

    absolute_episode_numbers: list[int] | None | Unset
    if isinstance(self.absolute_episode_numbers, Unset):
      absolute_episode_numbers = UNSET
    elif isinstance(self.absolute_episode_numbers, list):
      absolute_episode_numbers = self.absolute_episode_numbers

    else:
      absolute_episode_numbers = self.absolute_episode_numbers

    special_absolute_episode_numbers: list[float] | None | Unset
    if isinstance(self.special_absolute_episode_numbers, Unset):
      special_absolute_episode_numbers = UNSET
    elif isinstance(self.special_absolute_episode_numbers, list):
      special_absolute_episode_numbers = self.special_absolute_episode_numbers

    else:
      special_absolute_episode_numbers = self.special_absolute_episode_numbers

    air_date: None | str | Unset
    if isinstance(self.air_date, Unset):
      air_date = UNSET
    else:
      air_date = self.air_date

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

    full_season = self.full_season

    is_partial_season = self.is_partial_season

    is_multi_season = self.is_multi_season

    is_season_extra = self.is_season_extra

    is_split_episode = self.is_split_episode

    is_mini_series = self.is_mini_series

    special = self.special

    release_group: None | str | Unset
    if isinstance(self.release_group, Unset):
      release_group = UNSET
    else:
      release_group = self.release_group

    release_hash: None | str | Unset
    if isinstance(self.release_hash, Unset):
      release_hash = UNSET
    else:
      release_hash = self.release_hash

    season_part = self.season_part

    release_tokens: None | str | Unset
    if isinstance(self.release_tokens, Unset):
      release_tokens = UNSET
    else:
      release_tokens = self.release_tokens

    daily_part: int | None | Unset
    if isinstance(self.daily_part, Unset):
      daily_part = UNSET
    else:
      daily_part = self.daily_part

    is_daily = self.is_daily

    is_absolute_numbering = self.is_absolute_numbering

    is_possible_special_episode = self.is_possible_special_episode

    is_possible_scene_season_special = self.is_possible_scene_season_special

    release_type: str | Unset = UNSET
    if not isinstance(self.release_type, Unset):
      release_type = self.release_type.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if release_title is not UNSET:
      field_dict["releaseTitle"] = release_title
    if series_title is not UNSET:
      field_dict["seriesTitle"] = series_title
    if series_title_info is not UNSET:
      field_dict["seriesTitleInfo"] = series_title_info
    if quality is not UNSET:
      field_dict["quality"] = quality
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if episode_numbers is not UNSET:
      field_dict["episodeNumbers"] = episode_numbers
    if absolute_episode_numbers is not UNSET:
      field_dict["absoluteEpisodeNumbers"] = absolute_episode_numbers
    if special_absolute_episode_numbers is not UNSET:
      field_dict["specialAbsoluteEpisodeNumbers"] = special_absolute_episode_numbers
    if air_date is not UNSET:
      field_dict["airDate"] = air_date
    if languages is not UNSET:
      field_dict["languages"] = languages
    if full_season is not UNSET:
      field_dict["fullSeason"] = full_season
    if is_partial_season is not UNSET:
      field_dict["isPartialSeason"] = is_partial_season
    if is_multi_season is not UNSET:
      field_dict["isMultiSeason"] = is_multi_season
    if is_season_extra is not UNSET:
      field_dict["isSeasonExtra"] = is_season_extra
    if is_split_episode is not UNSET:
      field_dict["isSplitEpisode"] = is_split_episode
    if is_mini_series is not UNSET:
      field_dict["isMiniSeries"] = is_mini_series
    if special is not UNSET:
      field_dict["special"] = special
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group
    if release_hash is not UNSET:
      field_dict["releaseHash"] = release_hash
    if season_part is not UNSET:
      field_dict["seasonPart"] = season_part
    if release_tokens is not UNSET:
      field_dict["releaseTokens"] = release_tokens
    if daily_part is not UNSET:
      field_dict["dailyPart"] = daily_part
    if is_daily is not UNSET:
      field_dict["isDaily"] = is_daily
    if is_absolute_numbering is not UNSET:
      field_dict["isAbsoluteNumbering"] = is_absolute_numbering
    if is_possible_special_episode is not UNSET:
      field_dict["isPossibleSpecialEpisode"] = is_possible_special_episode
    if is_possible_scene_season_special is not UNSET:
      field_dict["isPossibleSceneSeasonSpecial"] = is_possible_scene_season_special
    if release_type is not UNSET:
      field_dict["releaseType"] = release_type

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.language import Language
    from ..models.quality_model import QualityModel
    from ..models.series_title_info import SeriesTitleInfo

    d = dict(src_dict)

    def _parse_release_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_title = _parse_release_title(d.pop("releaseTitle", UNSET))

    def _parse_series_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    series_title = _parse_series_title(d.pop("seriesTitle", UNSET))

    _series_title_info = d.pop("seriesTitleInfo", UNSET)
    series_title_info: SeriesTitleInfo | Unset
    if isinstance(_series_title_info, Unset):
      series_title_info = UNSET
    else:
      series_title_info = SeriesTitleInfo.from_dict(_series_title_info)

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

    season_number = d.pop("seasonNumber", UNSET)

    def _parse_episode_numbers(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        episode_numbers_type_0 = cast(list[int], data)

        return episode_numbers_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    episode_numbers = _parse_episode_numbers(d.pop("episodeNumbers", UNSET))

    def _parse_absolute_episode_numbers(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        absolute_episode_numbers_type_0 = cast(list[int], data)

        return absolute_episode_numbers_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    absolute_episode_numbers = _parse_absolute_episode_numbers(
      d.pop("absoluteEpisodeNumbers", UNSET)
    )

    def _parse_special_absolute_episode_numbers(data: object) -> list[float] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        special_absolute_episode_numbers_type_0 = cast(list[float], data)

        return special_absolute_episode_numbers_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[float] | None | Unset, data)

    special_absolute_episode_numbers = _parse_special_absolute_episode_numbers(
      d.pop("specialAbsoluteEpisodeNumbers", UNSET)
    )

    def _parse_air_date(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    air_date = _parse_air_date(d.pop("airDate", UNSET))

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

    full_season = d.pop("fullSeason", UNSET)

    is_partial_season = d.pop("isPartialSeason", UNSET)

    is_multi_season = d.pop("isMultiSeason", UNSET)

    is_season_extra = d.pop("isSeasonExtra", UNSET)

    is_split_episode = d.pop("isSplitEpisode", UNSET)

    is_mini_series = d.pop("isMiniSeries", UNSET)

    special = d.pop("special", UNSET)

    def _parse_release_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_group = _parse_release_group(d.pop("releaseGroup", UNSET))

    def _parse_release_hash(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_hash = _parse_release_hash(d.pop("releaseHash", UNSET))

    season_part = d.pop("seasonPart", UNSET)

    def _parse_release_tokens(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_tokens = _parse_release_tokens(d.pop("releaseTokens", UNSET))

    def _parse_daily_part(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    daily_part = _parse_daily_part(d.pop("dailyPart", UNSET))

    is_daily = d.pop("isDaily", UNSET)

    is_absolute_numbering = d.pop("isAbsoluteNumbering", UNSET)

    is_possible_special_episode = d.pop("isPossibleSpecialEpisode", UNSET)

    is_possible_scene_season_special = d.pop("isPossibleSceneSeasonSpecial", UNSET)

    _release_type = d.pop("releaseType", UNSET)
    release_type: ReleaseType | Unset
    if isinstance(_release_type, Unset):
      release_type = UNSET
    else:
      release_type = ReleaseType(_release_type)

    parsed_episode_info = cls(
      release_title=release_title,
      series_title=series_title,
      series_title_info=series_title_info,
      quality=quality,
      season_number=season_number,
      episode_numbers=episode_numbers,
      absolute_episode_numbers=absolute_episode_numbers,
      special_absolute_episode_numbers=special_absolute_episode_numbers,
      air_date=air_date,
      languages=languages,
      full_season=full_season,
      is_partial_season=is_partial_season,
      is_multi_season=is_multi_season,
      is_season_extra=is_season_extra,
      is_split_episode=is_split_episode,
      is_mini_series=is_mini_series,
      special=special,
      release_group=release_group,
      release_hash=release_hash,
      season_part=season_part,
      release_tokens=release_tokens,
      daily_part=daily_part,
      is_daily=is_daily,
      is_absolute_numbering=is_absolute_numbering,
      is_possible_special_episode=is_possible_special_episode,
      is_possible_scene_season_special=is_possible_scene_season_special,
      release_type=release_type,
    )

    return parsed_episode_info
