from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.collection_movie_resource import CollectionMovieResource
  from ..models.media_cover import MediaCover


T = TypeVar("T", bound="CollectionResource")


@_attrs_define
class CollectionResource:
  """
  Attributes:
      id (int | Unset):
      title (None | str | Unset):
      sort_title (None | str | Unset):
      tmdb_id (int | Unset):
      images (list[MediaCover] | None | Unset):
      overview (None | str | Unset):
      monitored (bool | Unset):
      root_folder_path (None | str | Unset):
      quality_profile_id (int | Unset):
      search_on_add (bool | Unset):
      minimum_availability (MovieStatusType | Unset):
      movies (list[CollectionMovieResource] | None | Unset):
      missing_movies (int | Unset):
      tags (list[int] | None | Unset):
  """

  id: int | Unset = UNSET
  title: None | str | Unset = UNSET
  sort_title: None | str | Unset = UNSET
  tmdb_id: int | Unset = UNSET
  images: list[MediaCover] | None | Unset = UNSET
  overview: None | str | Unset = UNSET
  monitored: bool | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  quality_profile_id: int | Unset = UNSET
  search_on_add: bool | Unset = UNSET
  minimum_availability: MovieStatusType | Unset = UNSET
  movies: list[CollectionMovieResource] | None | Unset = UNSET
  missing_movies: int | Unset = UNSET
  tags: list[int] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    sort_title: None | str | Unset
    if isinstance(self.sort_title, Unset):
      sort_title = UNSET
    else:
      sort_title = self.sort_title

    tmdb_id = self.tmdb_id

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

    overview: None | str | Unset
    if isinstance(self.overview, Unset):
      overview = UNSET
    else:
      overview = self.overview

    monitored = self.monitored

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

    quality_profile_id = self.quality_profile_id

    search_on_add = self.search_on_add

    minimum_availability: str | Unset = UNSET
    if not isinstance(self.minimum_availability, Unset):
      minimum_availability = self.minimum_availability.value

    movies: list[dict[str, Any]] | None | Unset
    if isinstance(self.movies, Unset):
      movies = UNSET
    elif isinstance(self.movies, list):
      movies = []
      for movies_type_0_item_data in self.movies:
        movies_type_0_item = movies_type_0_item_data.to_dict()
        movies.append(movies_type_0_item)

    else:
      movies = self.movies

    missing_movies = self.missing_movies

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if title is not UNSET:
      field_dict["title"] = title
    if sort_title is not UNSET:
      field_dict["sortTitle"] = sort_title
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id
    if images is not UNSET:
      field_dict["images"] = images
    if overview is not UNSET:
      field_dict["overview"] = overview
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if search_on_add is not UNSET:
      field_dict["searchOnAdd"] = search_on_add
    if minimum_availability is not UNSET:
      field_dict["minimumAvailability"] = minimum_availability
    if movies is not UNSET:
      field_dict["movies"] = movies
    if missing_movies is not UNSET:
      field_dict["missingMovies"] = missing_movies
    if tags is not UNSET:
      field_dict["tags"] = tags

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.collection_movie_resource import CollectionMovieResource
    from ..models.media_cover import MediaCover

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    def _parse_sort_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sort_title = _parse_sort_title(d.pop("sortTitle", UNSET))

    tmdb_id = d.pop("tmdbId", UNSET)

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

    def _parse_overview(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    overview = _parse_overview(d.pop("overview", UNSET))

    monitored = d.pop("monitored", UNSET)

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

    quality_profile_id = d.pop("qualityProfileId", UNSET)

    search_on_add = d.pop("searchOnAdd", UNSET)

    _minimum_availability = d.pop("minimumAvailability", UNSET)
    minimum_availability: MovieStatusType | Unset
    if isinstance(_minimum_availability, Unset):
      minimum_availability = UNSET
    else:
      minimum_availability = MovieStatusType(_minimum_availability)

    def _parse_movies(data: object) -> list[CollectionMovieResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        movies_type_0 = []
        _movies_type_0 = data
        for movies_type_0_item_data in _movies_type_0:
          movies_type_0_item = CollectionMovieResource.from_dict(movies_type_0_item_data)

          movies_type_0.append(movies_type_0_item)

        return movies_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[CollectionMovieResource] | None | Unset, data)

    movies = _parse_movies(d.pop("movies", UNSET))

    missing_movies = d.pop("missingMovies", UNSET)

    def _parse_tags(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        tags_type_0 = cast(list[int], data)

        return tags_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    tags = _parse_tags(d.pop("tags", UNSET))

    collection_resource = cls(
      id=id,
      title=title,
      sort_title=sort_title,
      tmdb_id=tmdb_id,
      images=images,
      overview=overview,
      monitored=monitored,
      root_folder_path=root_folder_path,
      quality_profile_id=quality_profile_id,
      search_on_add=search_on_add,
      minimum_availability=minimum_availability,
      movies=movies,
      missing_movies=missing_movies,
      tags=tags,
    )

    return collection_resource
