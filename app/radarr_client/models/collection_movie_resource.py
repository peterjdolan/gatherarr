from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.media_cover import MediaCover
  from ..models.ratings import Ratings


T = TypeVar("T", bound="CollectionMovieResource")


@_attrs_define
class CollectionMovieResource:
  """
  Attributes:
      tmdb_id (int | Unset):
      imdb_id (None | str | Unset):
      title (None | str | Unset):
      clean_title (None | str | Unset):
      sort_title (None | str | Unset):
      status (MovieStatusType | Unset):
      overview (None | str | Unset):
      runtime (int | Unset):
      images (list[MediaCover] | None | Unset):
      year (int | Unset):
      ratings (Ratings | Unset):
      genres (list[str] | None | Unset):
      folder (None | str | Unset):
      is_existing (bool | Unset):
      is_excluded (bool | Unset):
  """

  tmdb_id: int | Unset = UNSET
  imdb_id: None | str | Unset = UNSET
  title: None | str | Unset = UNSET
  clean_title: None | str | Unset = UNSET
  sort_title: None | str | Unset = UNSET
  status: MovieStatusType | Unset = UNSET
  overview: None | str | Unset = UNSET
  runtime: int | Unset = UNSET
  images: list[MediaCover] | None | Unset = UNSET
  year: int | Unset = UNSET
  ratings: Ratings | Unset = UNSET
  genres: list[str] | None | Unset = UNSET
  folder: None | str | Unset = UNSET
  is_existing: bool | Unset = UNSET
  is_excluded: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    tmdb_id = self.tmdb_id

    imdb_id: None | str | Unset
    if isinstance(self.imdb_id, Unset):
      imdb_id = UNSET
    else:
      imdb_id = self.imdb_id

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    clean_title: None | str | Unset
    if isinstance(self.clean_title, Unset):
      clean_title = UNSET
    else:
      clean_title = self.clean_title

    sort_title: None | str | Unset
    if isinstance(self.sort_title, Unset):
      sort_title = UNSET
    else:
      sort_title = self.sort_title

    status: str | Unset = UNSET
    if not isinstance(self.status, Unset):
      status = self.status.value

    overview: None | str | Unset
    if isinstance(self.overview, Unset):
      overview = UNSET
    else:
      overview = self.overview

    runtime = self.runtime

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

    year = self.year

    ratings: dict[str, Any] | Unset = UNSET
    if not isinstance(self.ratings, Unset):
      ratings = self.ratings.to_dict()

    genres: list[str] | None | Unset
    if isinstance(self.genres, Unset):
      genres = UNSET
    elif isinstance(self.genres, list):
      genres = self.genres

    else:
      genres = self.genres

    folder: None | str | Unset
    if isinstance(self.folder, Unset):
      folder = UNSET
    else:
      folder = self.folder

    is_existing = self.is_existing

    is_excluded = self.is_excluded

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id
    if imdb_id is not UNSET:
      field_dict["imdbId"] = imdb_id
    if title is not UNSET:
      field_dict["title"] = title
    if clean_title is not UNSET:
      field_dict["cleanTitle"] = clean_title
    if sort_title is not UNSET:
      field_dict["sortTitle"] = sort_title
    if status is not UNSET:
      field_dict["status"] = status
    if overview is not UNSET:
      field_dict["overview"] = overview
    if runtime is not UNSET:
      field_dict["runtime"] = runtime
    if images is not UNSET:
      field_dict["images"] = images
    if year is not UNSET:
      field_dict["year"] = year
    if ratings is not UNSET:
      field_dict["ratings"] = ratings
    if genres is not UNSET:
      field_dict["genres"] = genres
    if folder is not UNSET:
      field_dict["folder"] = folder
    if is_existing is not UNSET:
      field_dict["isExisting"] = is_existing
    if is_excluded is not UNSET:
      field_dict["isExcluded"] = is_excluded

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.media_cover import MediaCover
    from ..models.ratings import Ratings

    d = dict(src_dict)
    tmdb_id = d.pop("tmdbId", UNSET)

    def _parse_imdb_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    imdb_id = _parse_imdb_id(d.pop("imdbId", UNSET))

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    def _parse_clean_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    clean_title = _parse_clean_title(d.pop("cleanTitle", UNSET))

    def _parse_sort_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sort_title = _parse_sort_title(d.pop("sortTitle", UNSET))

    _status = d.pop("status", UNSET)
    status: MovieStatusType | Unset
    if isinstance(_status, Unset):
      status = UNSET
    else:
      status = MovieStatusType(_status)

    def _parse_overview(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    overview = _parse_overview(d.pop("overview", UNSET))

    runtime = d.pop("runtime", UNSET)

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

    year = d.pop("year", UNSET)

    _ratings = d.pop("ratings", UNSET)
    ratings: Ratings | Unset
    if isinstance(_ratings, Unset):
      ratings = UNSET
    else:
      ratings = Ratings.from_dict(_ratings)

    def _parse_genres(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        genres_type_0 = cast(list[str], data)

        return genres_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    genres = _parse_genres(d.pop("genres", UNSET))

    def _parse_folder(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    folder = _parse_folder(d.pop("folder", UNSET))

    is_existing = d.pop("isExisting", UNSET)

    is_excluded = d.pop("isExcluded", UNSET)

    collection_movie_resource = cls(
      tmdb_id=tmdb_id,
      imdb_id=imdb_id,
      title=title,
      clean_title=clean_title,
      sort_title=sort_title,
      status=status,
      overview=overview,
      runtime=runtime,
      images=images,
      year=year,
      ratings=ratings,
      genres=genres,
      folder=folder,
      is_existing=is_existing,
      is_excluded=is_excluded,
    )

    return collection_movie_resource
