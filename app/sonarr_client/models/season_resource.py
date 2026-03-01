from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.media_cover import MediaCover
  from ..models.season_statistics_resource import SeasonStatisticsResource


T = TypeVar("T", bound="SeasonResource")


@_attrs_define
class SeasonResource:
  """
  Attributes:
      season_number (int | Unset):
      monitored (bool | Unset):
      statistics (SeasonStatisticsResource | Unset):
      images (list[MediaCover] | None | Unset):
  """

  season_number: int | Unset = UNSET
  monitored: bool | Unset = UNSET
  statistics: SeasonStatisticsResource | Unset = UNSET
  images: list[MediaCover] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    season_number = self.season_number

    monitored = self.monitored

    statistics: dict[str, Any] | Unset = UNSET
    if not isinstance(self.statistics, Unset):
      statistics = self.statistics.to_dict()

    images: list[dict[str, Any]] | None | Unset
    if isinstance(self.images, Unset):
      images = UNSET
    elif isinstance(self.images, list):
      images = []
      for images_type_0_item_data in self.images:
        images_type_0_item = images_type_0_item_data.to_dict()
        images.append(images_type_0_item)

    else:
      images = self.images

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if statistics is not UNSET:
      field_dict["statistics"] = statistics
    if images is not UNSET:
      field_dict["images"] = images

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.media_cover import MediaCover
    from ..models.season_statistics_resource import SeasonStatisticsResource

    d = dict(src_dict)
    season_number = d.pop("seasonNumber", UNSET)

    monitored = d.pop("monitored", UNSET)

    _statistics = d.pop("statistics", UNSET)
    statistics: SeasonStatisticsResource | Unset
    if isinstance(_statistics, Unset):
      statistics = UNSET
    else:
      statistics = SeasonStatisticsResource.from_dict(_statistics)

    def _parse_images(data: object) -> list[MediaCover] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        images_type_0 = []
        _images_type_0 = data
        for images_type_0_item_data in _images_type_0:
          images_type_0_item = MediaCover.from_dict(images_type_0_item_data)

          images_type_0.append(images_type_0_item)

        return images_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[MediaCover] | None | Unset, data)

    images = _parse_images(d.pop("images", UNSET))

    season_resource = cls(
      season_number=season_number,
      monitored=monitored,
      statistics=statistics,
      images=images,
    )

    return season_resource
