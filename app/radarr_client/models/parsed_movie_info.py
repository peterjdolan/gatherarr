from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.language import Language
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="ParsedMovieInfo")


@_attrs_define
class ParsedMovieInfo:
  """
  Attributes:
      movie_titles (list[str] | None | Unset):
      original_title (None | str | Unset):
      release_title (None | str | Unset):
      simple_release_title (None | str | Unset):
      quality (QualityModel | Unset):
      languages (list[Language] | None | Unset):
      release_group (None | str | Unset):
      release_hash (None | str | Unset):
      edition (None | str | Unset):
      year (int | Unset):
      imdb_id (None | str | Unset):
      tmdb_id (int | Unset):
      hardcoded_subs (None | str | Unset):
      movie_title (None | str | Unset):
      primary_movie_title (None | str | Unset):
  """

  movie_titles: list[str] | None | Unset = UNSET
  original_title: None | str | Unset = UNSET
  release_title: None | str | Unset = UNSET
  simple_release_title: None | str | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  release_group: None | str | Unset = UNSET
  release_hash: None | str | Unset = UNSET
  edition: None | str | Unset = UNSET
  year: int | Unset = UNSET
  imdb_id: None | str | Unset = UNSET
  tmdb_id: int | Unset = UNSET
  hardcoded_subs: None | str | Unset = UNSET
  movie_title: None | str | Unset = UNSET
  primary_movie_title: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    movie_titles: list[str] | None | Unset
    if isinstance(self.movie_titles, Unset):
      movie_titles = UNSET
    elif isinstance(self.movie_titles, list):
      movie_titles = self.movie_titles

    else:
      movie_titles = self.movie_titles

    original_title: None | str | Unset
    if isinstance(self.original_title, Unset):
      original_title = UNSET
    else:
      original_title = self.original_title

    release_title: None | str | Unset
    if isinstance(self.release_title, Unset):
      release_title = UNSET
    else:
      release_title = self.release_title

    simple_release_title: None | str | Unset
    if isinstance(self.simple_release_title, Unset):
      simple_release_title = UNSET
    else:
      simple_release_title = self.simple_release_title

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    languages: list[dict[str, Any]] | None | Unset
    if isinstance(self.languages, Unset):
      languages = UNSET
    elif isinstance(self.languages, list):
      languages = []
      for languages_type_0_item_data in self.languages:
        languages_type_0_item = languages_type_0_item_data.to_dict()
        languages.append(languages_type_0_item)

    else:
      languages = self.languages

    release_group: None | str | Unset
    if isinstance(self.release_group, Unset):
      release_group = UNSET
    else:
      release_group = self.release_group

    release_hash: None | str | Unset
    if isinstance(self.release_hash, Unset):
      release_hash = UNSET
    else:
      release_hash = self.release_hash

    edition: None | str | Unset
    if isinstance(self.edition, Unset):
      edition = UNSET
    else:
      edition = self.edition

    year = self.year

    imdb_id: None | str | Unset
    if isinstance(self.imdb_id, Unset):
      imdb_id = UNSET
    else:
      imdb_id = self.imdb_id

    tmdb_id = self.tmdb_id

    hardcoded_subs: None | str | Unset
    if isinstance(self.hardcoded_subs, Unset):
      hardcoded_subs = UNSET
    else:
      hardcoded_subs = self.hardcoded_subs

    movie_title: None | str | Unset
    if isinstance(self.movie_title, Unset):
      movie_title = UNSET
    else:
      movie_title = self.movie_title

    primary_movie_title: None | str | Unset
    if isinstance(self.primary_movie_title, Unset):
      primary_movie_title = UNSET
    else:
      primary_movie_title = self.primary_movie_title

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if movie_titles is not UNSET:
      field_dict["movieTitles"] = movie_titles
    if original_title is not UNSET:
      field_dict["originalTitle"] = original_title
    if release_title is not UNSET:
      field_dict["releaseTitle"] = release_title
    if simple_release_title is not UNSET:
      field_dict["simpleReleaseTitle"] = simple_release_title
    if quality is not UNSET:
      field_dict["quality"] = quality
    if languages is not UNSET:
      field_dict["languages"] = languages
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group
    if release_hash is not UNSET:
      field_dict["releaseHash"] = release_hash
    if edition is not UNSET:
      field_dict["edition"] = edition
    if year is not UNSET:
      field_dict["year"] = year
    if imdb_id is not UNSET:
      field_dict["imdbId"] = imdb_id
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id
    if hardcoded_subs is not UNSET:
      field_dict["hardcodedSubs"] = hardcoded_subs
    if movie_title is not UNSET:
      field_dict["movieTitle"] = movie_title
    if primary_movie_title is not UNSET:
      field_dict["primaryMovieTitle"] = primary_movie_title

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.language import Language
    from ..models.quality_model import QualityModel

    d = dict(src_dict)

    def _parse_movie_titles(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        movie_titles_type_0 = cast(list[str], data)

        return movie_titles_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    movie_titles = _parse_movie_titles(d.pop("movieTitles", UNSET))

    def _parse_original_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    original_title = _parse_original_title(d.pop("originalTitle", UNSET))

    def _parse_release_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_title = _parse_release_title(d.pop("releaseTitle", UNSET))

    def _parse_simple_release_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    simple_release_title = _parse_simple_release_title(d.pop("simpleReleaseTitle", UNSET))

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

    def _parse_languages(data: object) -> list[Language] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        languages_type_0 = []
        _languages_type_0 = data
        for languages_type_0_item_data in _languages_type_0:
          languages_type_0_item = Language.from_dict(languages_type_0_item_data)

          languages_type_0.append(languages_type_0_item)

        return languages_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[Language] | None | Unset, data)

    languages = _parse_languages(d.pop("languages", UNSET))

    def _parse_release_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_group = _parse_release_group(d.pop("releaseGroup", UNSET))

    def _parse_release_hash(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_hash = _parse_release_hash(d.pop("releaseHash", UNSET))

    def _parse_edition(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    edition = _parse_edition(d.pop("edition", UNSET))

    year = d.pop("year", UNSET)

    def _parse_imdb_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    imdb_id = _parse_imdb_id(d.pop("imdbId", UNSET))

    tmdb_id = d.pop("tmdbId", UNSET)

    def _parse_hardcoded_subs(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    hardcoded_subs = _parse_hardcoded_subs(d.pop("hardcodedSubs", UNSET))

    def _parse_movie_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    movie_title = _parse_movie_title(d.pop("movieTitle", UNSET))

    def _parse_primary_movie_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    primary_movie_title = _parse_primary_movie_title(d.pop("primaryMovieTitle", UNSET))

    parsed_movie_info = cls(
      movie_titles=movie_titles,
      original_title=original_title,
      release_title=release_title,
      simple_release_title=simple_release_title,
      quality=quality,
      languages=languages,
      release_group=release_group,
      release_hash=release_hash,
      edition=edition,
      year=year,
      imdb_id=imdb_id,
      tmdb_id=tmdb_id,
      hardcoded_subs=hardcoded_subs,
      movie_title=movie_title,
      primary_movie_title=primary_movie_title,
    )

    return parsed_movie_info
