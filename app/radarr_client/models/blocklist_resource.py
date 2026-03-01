from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.download_protocol import DownloadProtocol
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.language import Language
  from ..models.movie_resource import MovieResource
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="BlocklistResource")


@_attrs_define
class BlocklistResource:
  """
  Attributes:
      id (int | Unset):
      movie_id (int | Unset):
      source_title (None | str | Unset):
      languages (list[Language] | None | Unset):
      quality (QualityModel | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      date (datetime.datetime | Unset):
      protocol (DownloadProtocol | Unset):
      indexer (None | str | Unset):
      message (None | str | Unset):
      movie (MovieResource | Unset):
  """

  id: int | Unset = UNSET
  movie_id: int | Unset = UNSET
  source_title: None | str | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  date: datetime.datetime | Unset = UNSET
  protocol: DownloadProtocol | Unset = UNSET
  indexer: None | str | Unset = UNSET
  message: None | str | Unset = UNSET
  movie: MovieResource | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    movie_id = self.movie_id

    source_title: None | str | Unset
    if isinstance(self.source_title, Unset):
      source_title = UNSET
    else:
      source_title = self.source_title

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

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

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

    date: str | Unset = UNSET
    if not isinstance(self.date, Unset):
      date = self.date.isoformat()

    protocol: str | Unset = UNSET
    if not isinstance(self.protocol, Unset):
      protocol = self.protocol.value

    indexer: None | str | Unset
    if isinstance(self.indexer, Unset):
      indexer = UNSET
    else:
      indexer = self.indexer

    message: None | str | Unset
    if isinstance(self.message, Unset):
      message = UNSET
    else:
      message = self.message

    movie: dict[str, Any] | Unset = UNSET
    if not isinstance(self.movie, Unset):
      movie = self.movie.to_dict()

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if movie_id is not UNSET:
      field_dict["movieId"] = movie_id
    if source_title is not UNSET:
      field_dict["sourceTitle"] = source_title
    if languages is not UNSET:
      field_dict["languages"] = languages
    if quality is not UNSET:
      field_dict["quality"] = quality
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if date is not UNSET:
      field_dict["date"] = date
    if protocol is not UNSET:
      field_dict["protocol"] = protocol
    if indexer is not UNSET:
      field_dict["indexer"] = indexer
    if message is not UNSET:
      field_dict["message"] = message
    if movie is not UNSET:
      field_dict["movie"] = movie

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.language import Language
    from ..models.movie_resource import MovieResource
    from ..models.quality_model import QualityModel

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    movie_id = d.pop("movieId", UNSET)

    def _parse_source_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    source_title = _parse_source_title(d.pop("sourceTitle", UNSET))

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

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

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

    _date = d.pop("date", UNSET)
    date: datetime.datetime | Unset
    if isinstance(_date, Unset):
      date = UNSET
    else:
      date = isoparse(_date)

    _protocol = d.pop("protocol", UNSET)
    protocol: DownloadProtocol | Unset
    if isinstance(_protocol, Unset):
      protocol = UNSET
    else:
      protocol = DownloadProtocol(_protocol)

    def _parse_indexer(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    indexer = _parse_indexer(d.pop("indexer", UNSET))

    def _parse_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    message = _parse_message(d.pop("message", UNSET))

    _movie = d.pop("movie", UNSET)
    movie: MovieResource | Unset
    if isinstance(_movie, Unset):
      movie = UNSET
    else:
      movie = MovieResource.from_dict(_movie)

    blocklist_resource = cls(
      id=id,
      movie_id=movie_id,
      source_title=source_title,
      languages=languages,
      quality=quality,
      custom_formats=custom_formats,
      date=date,
      protocol=protocol,
      indexer=indexer,
      message=message,
      movie=movie,
    )

    return blocklist_resource
