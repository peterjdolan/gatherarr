from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.language import Language
  from ..models.movie_resource import MovieResource
  from ..models.parsed_movie_info import ParsedMovieInfo


T = TypeVar("T", bound="ParseResource")


@_attrs_define
class ParseResource:
  """
  Attributes:
      id (int | Unset):
      title (None | str | Unset):
      parsed_movie_info (ParsedMovieInfo | Unset):
      movie (MovieResource | Unset):
      languages (list[Language] | None | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      custom_format_score (int | Unset):
  """

  id: int | Unset = UNSET
  title: None | str | Unset = UNSET
  parsed_movie_info: ParsedMovieInfo | Unset = UNSET
  movie: MovieResource | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  custom_format_score: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    parsed_movie_info: dict[str, Any] | Unset = UNSET
    if not isinstance(self.parsed_movie_info, Unset):
      parsed_movie_info = self.parsed_movie_info.to_dict()

    movie: dict[str, Any] | Unset = UNSET
    if not isinstance(self.movie, Unset):
      movie = self.movie.to_dict()

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

    custom_formats: list[dict[str, Any]] | None | Unset
    if isinstance(self.custom_formats, Unset):
      custom_formats = UNSET
    elif isinstance(self.custom_formats, list):
      custom_formats = []
      for custom_formats_type_0_item_data in self.custom_formats:
        custom_formats_type_0_item = custom_formats_type_0_item_data.to_dict()
        custom_formats.append(custom_formats_type_0_item)

    else:
      custom_formats = self.custom_formats

    custom_format_score = self.custom_format_score

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if title is not UNSET:
      field_dict["title"] = title
    if parsed_movie_info is not UNSET:
      field_dict["parsedMovieInfo"] = parsed_movie_info
    if movie is not UNSET:
      field_dict["movie"] = movie
    if languages is not UNSET:
      field_dict["languages"] = languages
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if custom_format_score is not UNSET:
      field_dict["customFormatScore"] = custom_format_score

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.language import Language
    from ..models.movie_resource import MovieResource
    from ..models.parsed_movie_info import ParsedMovieInfo

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    _parsed_movie_info = d.pop("parsedMovieInfo", UNSET)
    parsed_movie_info: ParsedMovieInfo | Unset
    if isinstance(_parsed_movie_info, Unset):
      parsed_movie_info = UNSET
    else:
      parsed_movie_info = ParsedMovieInfo.from_dict(_parsed_movie_info)

    _movie = d.pop("movie", UNSET)
    movie: MovieResource | Unset
    if isinstance(_movie, Unset):
      movie = UNSET
    else:
      movie = MovieResource.from_dict(_movie)

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

    def _parse_custom_formats(data: object) -> list[CustomFormatResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        custom_formats_type_0 = []
        _custom_formats_type_0 = data
        for custom_formats_type_0_item_data in _custom_formats_type_0:
          custom_formats_type_0_item = CustomFormatResource.from_dict(
            custom_formats_type_0_item_data
          )

          custom_formats_type_0.append(custom_formats_type_0_item)

        return custom_formats_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[CustomFormatResource] | None | Unset, data)

    custom_formats = _parse_custom_formats(d.pop("customFormats", UNSET))

    custom_format_score = d.pop("customFormatScore", UNSET)

    parse_resource = cls(
      id=id,
      title=title,
      parsed_movie_info=parsed_movie_info,
      movie=movie,
      languages=languages,
      custom_formats=custom_formats,
      custom_format_score=custom_format_score,
    )

    return parse_resource
