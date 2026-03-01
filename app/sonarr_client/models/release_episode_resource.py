from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReleaseEpisodeResource")


@_attrs_define
class ReleaseEpisodeResource:
  """
  Attributes:
      id (int | Unset):
      season_number (int | Unset):
      episode_number (int | Unset):
      absolute_episode_number (int | None | Unset):
      title (None | str | Unset):
  """

  id: int | Unset = UNSET
  season_number: int | Unset = UNSET
  episode_number: int | Unset = UNSET
  absolute_episode_number: int | None | Unset = UNSET
  title: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    season_number = self.season_number

    episode_number = self.episode_number

    absolute_episode_number: int | None | Unset
    if isinstance(self.absolute_episode_number, Unset):
      absolute_episode_number = UNSET
    else:
      absolute_episode_number = self.absolute_episode_number

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if episode_number is not UNSET:
      field_dict["episodeNumber"] = episode_number
    if absolute_episode_number is not UNSET:
      field_dict["absoluteEpisodeNumber"] = absolute_episode_number
    if title is not UNSET:
      field_dict["title"] = title

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    season_number = d.pop("seasonNumber", UNSET)

    episode_number = d.pop("episodeNumber", UNSET)

    def _parse_absolute_episode_number(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    absolute_episode_number = _parse_absolute_episode_number(d.pop("absoluteEpisodeNumber", UNSET))

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    release_episode_resource = cls(
      id=id,
      season_number=season_number,
      episode_number=episode_number,
      absolute_episode_number=absolute_episode_number,
      title=title,
    )

    return release_episode_resource
