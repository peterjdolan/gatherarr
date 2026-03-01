from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RenameEpisodeResource")


@_attrs_define
class RenameEpisodeResource:
  """
  Attributes:
      id (int | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      episode_numbers (list[int] | None | Unset):
      episode_file_id (int | Unset):
      existing_path (None | str | Unset):
      new_path (None | str | Unset):
  """

  id: int | Unset = UNSET
  series_id: int | Unset = UNSET
  season_number: int | Unset = UNSET
  episode_numbers: list[int] | None | Unset = UNSET
  episode_file_id: int | Unset = UNSET
  existing_path: None | str | Unset = UNSET
  new_path: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    series_id = self.series_id

    season_number = self.season_number

    episode_numbers: list[int] | None | Unset
    if isinstance(self.episode_numbers, Unset):
      episode_numbers = UNSET
    elif isinstance(self.episode_numbers, list):
      episode_numbers = self.episode_numbers

    else:
      episode_numbers = self.episode_numbers

    episode_file_id = self.episode_file_id

    existing_path: None | str | Unset
    if isinstance(self.existing_path, Unset):
      existing_path = UNSET
    else:
      existing_path = self.existing_path

    new_path: None | str | Unset
    if isinstance(self.new_path, Unset):
      new_path = UNSET
    else:
      new_path = self.new_path

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if series_id is not UNSET:
      field_dict["seriesId"] = series_id
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if episode_numbers is not UNSET:
      field_dict["episodeNumbers"] = episode_numbers
    if episode_file_id is not UNSET:
      field_dict["episodeFileId"] = episode_file_id
    if existing_path is not UNSET:
      field_dict["existingPath"] = existing_path
    if new_path is not UNSET:
      field_dict["newPath"] = new_path

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    series_id = d.pop("seriesId", UNSET)

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

    episode_file_id = d.pop("episodeFileId", UNSET)

    def _parse_existing_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    existing_path = _parse_existing_path(d.pop("existingPath", UNSET))

    def _parse_new_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    new_path = _parse_new_path(d.pop("newPath", UNSET))

    rename_episode_resource = cls(
      id=id,
      series_id=series_id,
      season_number=season_number,
      episode_numbers=episode_numbers,
      episode_file_id=episode_file_id,
      existing_path=existing_path,
      new_path=new_path,
    )

    return rename_episode_resource
