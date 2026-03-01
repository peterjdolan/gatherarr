from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.extra_file_type import ExtraFileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtraFileResource")


@_attrs_define
class ExtraFileResource:
  """
  Attributes:
      id (int | Unset):
      movie_id (int | Unset):
      movie_file_id (int | None | Unset):
      relative_path (None | str | Unset):
      extension (None | str | Unset):
      language_tags (list[str] | None | Unset):
      title (None | str | Unset):
      type_ (ExtraFileType | Unset):
  """

  id: int | Unset = UNSET
  movie_id: int | Unset = UNSET
  movie_file_id: int | None | Unset = UNSET
  relative_path: None | str | Unset = UNSET
  extension: None | str | Unset = UNSET
  language_tags: list[str] | None | Unset = UNSET
  title: None | str | Unset = UNSET
  type_: ExtraFileType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    movie_id = self.movie_id

    movie_file_id: int | None | Unset
    if isinstance(self.movie_file_id, Unset):
      movie_file_id = UNSET
    else:
      movie_file_id = self.movie_file_id

    relative_path: None | str | Unset
    if isinstance(self.relative_path, Unset):
      relative_path = UNSET
    else:
      relative_path = self.relative_path

    extension: None | str | Unset
    if isinstance(self.extension, Unset):
      extension = UNSET
    else:
      extension = self.extension

    language_tags: list[str] | None | Unset
    if isinstance(self.language_tags, Unset):
      language_tags = UNSET
    elif isinstance(self.language_tags, list):
      language_tags = self.language_tags

    else:
      language_tags = self.language_tags

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if movie_id is not UNSET:
      field_dict["movieId"] = movie_id
    if movie_file_id is not UNSET:
      field_dict["movieFileId"] = movie_file_id
    if relative_path is not UNSET:
      field_dict["relativePath"] = relative_path
    if extension is not UNSET:
      field_dict["extension"] = extension
    if language_tags is not UNSET:
      field_dict["languageTags"] = language_tags
    if title is not UNSET:
      field_dict["title"] = title
    if type_ is not UNSET:
      field_dict["type"] = type_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    movie_id = d.pop("movieId", UNSET)

    def _parse_movie_file_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    movie_file_id = _parse_movie_file_id(d.pop("movieFileId", UNSET))

    def _parse_relative_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    relative_path = _parse_relative_path(d.pop("relativePath", UNSET))

    def _parse_extension(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    extension = _parse_extension(d.pop("extension", UNSET))

    def _parse_language_tags(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        language_tags_type_0 = cast(list[str], data)

        return language_tags_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    language_tags = _parse_language_tags(d.pop("languageTags", UNSET))

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    _type_ = d.pop("type", UNSET)
    type_: ExtraFileType | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = ExtraFileType(_type_)

    extra_file_resource = cls(
      id=id,
      movie_id=movie_id,
      movie_file_id=movie_file_id,
      relative_path=relative_path,
      extension=extension,
      language_tags=language_tags,
      title=title,
      type_=type_,
    )

    return extra_file_resource
