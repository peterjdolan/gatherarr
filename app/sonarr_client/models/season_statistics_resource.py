from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeasonStatisticsResource")


@_attrs_define
class SeasonStatisticsResource:
  """
  Attributes:
      next_airing (datetime.datetime | None | Unset):
      previous_airing (datetime.datetime | None | Unset):
      episode_file_count (int | Unset):
      episode_count (int | Unset):
      total_episode_count (int | Unset):
      size_on_disk (int | Unset):
      release_groups (list[str] | None | Unset):
      percent_of_episodes (float | Unset):
  """

  next_airing: datetime.datetime | None | Unset = UNSET
  previous_airing: datetime.datetime | None | Unset = UNSET
  episode_file_count: int | Unset = UNSET
  episode_count: int | Unset = UNSET
  total_episode_count: int | Unset = UNSET
  size_on_disk: int | Unset = UNSET
  release_groups: list[str] | None | Unset = UNSET
  percent_of_episodes: float | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    next_airing: None | str | Unset
    if isinstance(self.next_airing, Unset):
      next_airing = UNSET
    elif isinstance(self.next_airing, datetime.datetime):
      next_airing = self.next_airing.isoformat()
    else:
      next_airing = self.next_airing

    previous_airing: None | str | Unset
    if isinstance(self.previous_airing, Unset):
      previous_airing = UNSET
    elif isinstance(self.previous_airing, datetime.datetime):
      previous_airing = self.previous_airing.isoformat()
    else:
      previous_airing = self.previous_airing

    episode_file_count = self.episode_file_count

    episode_count = self.episode_count

    total_episode_count = self.total_episode_count

    size_on_disk = self.size_on_disk

    release_groups: list[str] | None | Unset
    if isinstance(self.release_groups, Unset):
      release_groups = UNSET
    elif isinstance(self.release_groups, list):
      release_groups = self.release_groups

    else:
      release_groups = self.release_groups

    percent_of_episodes = self.percent_of_episodes

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if next_airing is not UNSET:
      field_dict["nextAiring"] = next_airing
    if previous_airing is not UNSET:
      field_dict["previousAiring"] = previous_airing
    if episode_file_count is not UNSET:
      field_dict["episodeFileCount"] = episode_file_count
    if episode_count is not UNSET:
      field_dict["episodeCount"] = episode_count
    if total_episode_count is not UNSET:
      field_dict["totalEpisodeCount"] = total_episode_count
    if size_on_disk is not UNSET:
      field_dict["sizeOnDisk"] = size_on_disk
    if release_groups is not UNSET:
      field_dict["releaseGroups"] = release_groups
    if percent_of_episodes is not UNSET:
      field_dict["percentOfEpisodes"] = percent_of_episodes

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_next_airing(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        next_airing_type_0 = isoparse(data)

        return next_airing_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    next_airing = _parse_next_airing(d.pop("nextAiring", UNSET))

    def _parse_previous_airing(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        previous_airing_type_0 = isoparse(data)

        return previous_airing_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    previous_airing = _parse_previous_airing(d.pop("previousAiring", UNSET))

    episode_file_count = d.pop("episodeFileCount", UNSET)

    episode_count = d.pop("episodeCount", UNSET)

    total_episode_count = d.pop("totalEpisodeCount", UNSET)

    size_on_disk = d.pop("sizeOnDisk", UNSET)

    def _parse_release_groups(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        release_groups_type_0 = cast(list[str], data)

        return release_groups_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    release_groups = _parse_release_groups(d.pop("releaseGroups", UNSET))

    percent_of_episodes = d.pop("percentOfEpisodes", UNSET)

    season_statistics_resource = cls(
      next_airing=next_airing,
      previous_airing=previous_airing,
      episode_file_count=episode_file_count,
      episode_count=episode_count,
      total_episode_count=total_episode_count,
      size_on_disk=size_on_disk,
      release_groups=release_groups,
      percent_of_episodes=percent_of_episodes,
    )

    return season_statistics_resource
