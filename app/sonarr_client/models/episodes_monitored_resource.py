from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="EpisodesMonitoredResource")


@_attrs_define
class EpisodesMonitoredResource:
  """
  Attributes:
      episode_ids (list[int] | None | Unset):
      monitored (bool | Unset):
  """

  episode_ids: list[int] | None | Unset = UNSET
  monitored: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    episode_ids: list[int] | None | Unset
    if isinstance(self.episode_ids, Unset):
      episode_ids = UNSET
    elif isinstance(self.episode_ids, list):
      episode_ids = self.episode_ids

    else:
      episode_ids = self.episode_ids

    monitored = self.monitored

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if episode_ids is not UNSET:
      field_dict["episodeIds"] = episode_ids
    if monitored is not UNSET:
      field_dict["monitored"] = monitored

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

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

    monitored = d.pop("monitored", UNSET)

    episodes_monitored_resource = cls(
      episode_ids=episode_ids,
      monitored=monitored,
    )

    return episodes_monitored_resource
