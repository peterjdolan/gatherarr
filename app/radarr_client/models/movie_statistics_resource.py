from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MovieStatisticsResource")


@_attrs_define
class MovieStatisticsResource:
  """
  Attributes:
      movie_file_count (int | Unset):
      size_on_disk (int | Unset):
      release_groups (list[str] | None | Unset):
  """

  movie_file_count: int | Unset = UNSET
  size_on_disk: int | Unset = UNSET
  release_groups: list[str] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    movie_file_count = self.movie_file_count

    size_on_disk = self.size_on_disk

    release_groups: list[str] | None | Unset
    if isinstance(self.release_groups, Unset):
      release_groups = UNSET
    elif isinstance(self.release_groups, list):
      release_groups = self.release_groups

    else:
      release_groups = self.release_groups

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if movie_file_count is not UNSET:
      field_dict["movieFileCount"] = movie_file_count
    if size_on_disk is not UNSET:
      field_dict["sizeOnDisk"] = size_on_disk
    if release_groups is not UNSET:
      field_dict["releaseGroups"] = release_groups

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    movie_file_count = d.pop("movieFileCount", UNSET)

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

    movie_statistics_resource = cls(
      movie_file_count=movie_file_count,
      size_on_disk=size_on_disk,
      release_groups=release_groups,
    )

    return movie_statistics_resource
