from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.season_resource import SeasonResource


T = TypeVar("T", bound="SeasonPassSeriesResource")


@_attrs_define
class SeasonPassSeriesResource:
  """
  Attributes:
      id (int | Unset):
      monitored (bool | None | Unset):
      seasons (list[SeasonResource] | None | Unset):
  """

  id: int | Unset = UNSET
  monitored: bool | None | Unset = UNSET
  seasons: list[SeasonResource] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    monitored: bool | None | Unset
    if isinstance(self.monitored, Unset):
      monitored = UNSET
    else:
      monitored = self.monitored

    seasons: list[dict[str, Any]] | None | Unset
    if isinstance(self.seasons, Unset):
      seasons = UNSET
    elif isinstance(self.seasons, list):
      seasons = []
      for seasons_type_0_item_data in self.seasons:
        seasons_type_0_item = seasons_type_0_item_data.to_dict()
        seasons.append(seasons_type_0_item)

    else:
      seasons = self.seasons

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if seasons is not UNSET:
      field_dict["seasons"] = seasons

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.season_resource import SeasonResource

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_monitored(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    monitored = _parse_monitored(d.pop("monitored", UNSET))

    def _parse_seasons(data: object) -> list[SeasonResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        seasons_type_0 = []
        _seasons_type_0 = data
        for seasons_type_0_item_data in _seasons_type_0:
          seasons_type_0_item = SeasonResource.from_dict(seasons_type_0_item_data)

          seasons_type_0.append(seasons_type_0_item)

        return seasons_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[SeasonResource] | None | Unset, data)

    seasons = _parse_seasons(d.pop("seasons", UNSET))

    season_pass_series_resource = cls(
      id=id,
      monitored=monitored,
      seasons=seasons,
    )

    return season_pass_series_resource
