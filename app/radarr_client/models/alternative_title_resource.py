from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.source_type import SourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlternativeTitleResource")


@_attrs_define
class AlternativeTitleResource:
  """
  Attributes:
      id (int | Unset):
      source_type (SourceType | Unset):
      movie_metadata_id (int | Unset):
      title (None | str | Unset):
      clean_title (None | str | Unset):
  """

  id: int | Unset = UNSET
  source_type: SourceType | Unset = UNSET
  movie_metadata_id: int | Unset = UNSET
  title: None | str | Unset = UNSET
  clean_title: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    source_type: str | Unset = UNSET
    if not isinstance(self.source_type, Unset):
      source_type = self.source_type.value

    movie_metadata_id = self.movie_metadata_id

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

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if source_type is not UNSET:
      field_dict["sourceType"] = source_type
    if movie_metadata_id is not UNSET:
      field_dict["movieMetadataId"] = movie_metadata_id
    if title is not UNSET:
      field_dict["title"] = title
    if clean_title is not UNSET:
      field_dict["cleanTitle"] = clean_title

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    _source_type = d.pop("sourceType", UNSET)
    source_type: SourceType | Unset
    if isinstance(_source_type, Unset):
      source_type = UNSET
    else:
      source_type = SourceType(_source_type)

    movie_metadata_id = d.pop("movieMetadataId", UNSET)

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

    alternative_title_resource = cls(
      id=id,
      source_type=source_type,
      movie_metadata_id=movie_metadata_id,
      title=title,
      clean_title=clean_title,
    )

    return alternative_title_resource
