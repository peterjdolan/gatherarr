from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="NamingConfigResource")


@_attrs_define
class NamingConfigResource:
  """
  Attributes:
      id (int | Unset):
      rename_episodes (bool | Unset):
      replace_illegal_characters (bool | Unset):
      colon_replacement_format (int | Unset):
      custom_colon_replacement_format (None | str | Unset):
      multi_episode_style (int | Unset):
      standard_episode_format (None | str | Unset):
      daily_episode_format (None | str | Unset):
      anime_episode_format (None | str | Unset):
      series_folder_format (None | str | Unset):
      season_folder_format (None | str | Unset):
      specials_folder_format (None | str | Unset):
  """

  id: int | Unset = UNSET
  rename_episodes: bool | Unset = UNSET
  replace_illegal_characters: bool | Unset = UNSET
  colon_replacement_format: int | Unset = UNSET
  custom_colon_replacement_format: None | str | Unset = UNSET
  multi_episode_style: int | Unset = UNSET
  standard_episode_format: None | str | Unset = UNSET
  daily_episode_format: None | str | Unset = UNSET
  anime_episode_format: None | str | Unset = UNSET
  series_folder_format: None | str | Unset = UNSET
  season_folder_format: None | str | Unset = UNSET
  specials_folder_format: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    rename_episodes = self.rename_episodes

    replace_illegal_characters = self.replace_illegal_characters

    colon_replacement_format = self.colon_replacement_format

    custom_colon_replacement_format: None | str | Unset
    if isinstance(self.custom_colon_replacement_format, Unset):
      custom_colon_replacement_format = UNSET
    else:
      custom_colon_replacement_format = self.custom_colon_replacement_format

    multi_episode_style = self.multi_episode_style

    standard_episode_format: None | str | Unset
    if isinstance(self.standard_episode_format, Unset):
      standard_episode_format = UNSET
    else:
      standard_episode_format = self.standard_episode_format

    daily_episode_format: None | str | Unset
    if isinstance(self.daily_episode_format, Unset):
      daily_episode_format = UNSET
    else:
      daily_episode_format = self.daily_episode_format

    anime_episode_format: None | str | Unset
    if isinstance(self.anime_episode_format, Unset):
      anime_episode_format = UNSET
    else:
      anime_episode_format = self.anime_episode_format

    series_folder_format: None | str | Unset
    if isinstance(self.series_folder_format, Unset):
      series_folder_format = UNSET
    else:
      series_folder_format = self.series_folder_format

    season_folder_format: None | str | Unset
    if isinstance(self.season_folder_format, Unset):
      season_folder_format = UNSET
    else:
      season_folder_format = self.season_folder_format

    specials_folder_format: None | str | Unset
    if isinstance(self.specials_folder_format, Unset):
      specials_folder_format = UNSET
    else:
      specials_folder_format = self.specials_folder_format

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if rename_episodes is not UNSET:
      field_dict["renameEpisodes"] = rename_episodes
    if replace_illegal_characters is not UNSET:
      field_dict["replaceIllegalCharacters"] = replace_illegal_characters
    if colon_replacement_format is not UNSET:
      field_dict["colonReplacementFormat"] = colon_replacement_format
    if custom_colon_replacement_format is not UNSET:
      field_dict["customColonReplacementFormat"] = custom_colon_replacement_format
    if multi_episode_style is not UNSET:
      field_dict["multiEpisodeStyle"] = multi_episode_style
    if standard_episode_format is not UNSET:
      field_dict["standardEpisodeFormat"] = standard_episode_format
    if daily_episode_format is not UNSET:
      field_dict["dailyEpisodeFormat"] = daily_episode_format
    if anime_episode_format is not UNSET:
      field_dict["animeEpisodeFormat"] = anime_episode_format
    if series_folder_format is not UNSET:
      field_dict["seriesFolderFormat"] = series_folder_format
    if season_folder_format is not UNSET:
      field_dict["seasonFolderFormat"] = season_folder_format
    if specials_folder_format is not UNSET:
      field_dict["specialsFolderFormat"] = specials_folder_format

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    rename_episodes = d.pop("renameEpisodes", UNSET)

    replace_illegal_characters = d.pop("replaceIllegalCharacters", UNSET)

    colon_replacement_format = d.pop("colonReplacementFormat", UNSET)

    def _parse_custom_colon_replacement_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    custom_colon_replacement_format = _parse_custom_colon_replacement_format(
      d.pop("customColonReplacementFormat", UNSET)
    )

    multi_episode_style = d.pop("multiEpisodeStyle", UNSET)

    def _parse_standard_episode_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    standard_episode_format = _parse_standard_episode_format(d.pop("standardEpisodeFormat", UNSET))

    def _parse_daily_episode_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    daily_episode_format = _parse_daily_episode_format(d.pop("dailyEpisodeFormat", UNSET))

    def _parse_anime_episode_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    anime_episode_format = _parse_anime_episode_format(d.pop("animeEpisodeFormat", UNSET))

    def _parse_series_folder_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    series_folder_format = _parse_series_folder_format(d.pop("seriesFolderFormat", UNSET))

    def _parse_season_folder_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    season_folder_format = _parse_season_folder_format(d.pop("seasonFolderFormat", UNSET))

    def _parse_specials_folder_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    specials_folder_format = _parse_specials_folder_format(d.pop("specialsFolderFormat", UNSET))

    naming_config_resource = cls(
      id=id,
      rename_episodes=rename_episodes,
      replace_illegal_characters=replace_illegal_characters,
      colon_replacement_format=colon_replacement_format,
      custom_colon_replacement_format=custom_colon_replacement_format,
      multi_episode_style=multi_episode_style,
      standard_episode_format=standard_episode_format,
      daily_episode_format=daily_episode_format,
      anime_episode_format=anime_episode_format,
      series_folder_format=series_folder_format,
      season_folder_format=season_folder_format,
      specials_folder_format=specials_folder_format,
    )

    return naming_config_resource
