from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionUpdateResource")


@_attrs_define
class CollectionUpdateResource:
  """
  Attributes:
      collection_ids (list[int] | None | Unset):
      monitored (bool | None | Unset):
      monitor_movies (bool | None | Unset):
      search_on_add (bool | None | Unset):
      quality_profile_id (int | None | Unset):
      root_folder_path (None | str | Unset):
      minimum_availability (MovieStatusType | Unset):
  """

  collection_ids: list[int] | None | Unset = UNSET
  monitored: bool | None | Unset = UNSET
  monitor_movies: bool | None | Unset = UNSET
  search_on_add: bool | None | Unset = UNSET
  quality_profile_id: int | None | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  minimum_availability: MovieStatusType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    collection_ids: list[int] | None | Unset
    if isinstance(self.collection_ids, Unset):
      collection_ids = UNSET
    elif isinstance(self.collection_ids, list):
      collection_ids = self.collection_ids

    else:
      collection_ids = self.collection_ids

    monitored: bool | None | Unset
    if isinstance(self.monitored, Unset):
      monitored = UNSET
    else:
      monitored = self.monitored

    monitor_movies: bool | None | Unset
    if isinstance(self.monitor_movies, Unset):
      monitor_movies = UNSET
    else:
      monitor_movies = self.monitor_movies

    search_on_add: bool | None | Unset
    if isinstance(self.search_on_add, Unset):
      search_on_add = UNSET
    else:
      search_on_add = self.search_on_add

    quality_profile_id: int | None | Unset
    if isinstance(self.quality_profile_id, Unset):
      quality_profile_id = UNSET
    else:
      quality_profile_id = self.quality_profile_id

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

    minimum_availability: str | Unset = UNSET
    if not isinstance(self.minimum_availability, Unset):
      minimum_availability = self.minimum_availability.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if collection_ids is not UNSET:
      field_dict["collectionIds"] = collection_ids
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if monitor_movies is not UNSET:
      field_dict["monitorMovies"] = monitor_movies
    if search_on_add is not UNSET:
      field_dict["searchOnAdd"] = search_on_add
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if minimum_availability is not UNSET:
      field_dict["minimumAvailability"] = minimum_availability

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_collection_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        collection_ids_type_0 = cast(list[int], data)

        return collection_ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    collection_ids = _parse_collection_ids(d.pop("collectionIds", UNSET))

    def _parse_monitored(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    monitored = _parse_monitored(d.pop("monitored", UNSET))

    def _parse_monitor_movies(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    monitor_movies = _parse_monitor_movies(d.pop("monitorMovies", UNSET))

    def _parse_search_on_add(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    search_on_add = _parse_search_on_add(d.pop("searchOnAdd", UNSET))

    def _parse_quality_profile_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    quality_profile_id = _parse_quality_profile_id(d.pop("qualityProfileId", UNSET))

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

    _minimum_availability = d.pop("minimumAvailability", UNSET)
    minimum_availability: MovieStatusType | Unset
    if isinstance(_minimum_availability, Unset):
      minimum_availability = UNSET
    else:
      minimum_availability = MovieStatusType(_minimum_availability)

    collection_update_resource = cls(
      collection_ids=collection_ids,
      monitored=monitored,
      monitor_movies=monitor_movies,
      search_on_add=search_on_add,
      quality_profile_id=quality_profile_id,
      root_folder_path=root_folder_path,
      minimum_availability=minimum_availability,
    )

    return collection_update_resource
