from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MovieCollectionResource")


@_attrs_define
class MovieCollectionResource:
  """
  Attributes:
      title (None | str | Unset):
      tmdb_id (int | Unset):
  """

  title: None | str | Unset = UNSET
  tmdb_id: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    tmdb_id = self.tmdb_id

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if title is not UNSET:
      field_dict["title"] = title
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    tmdb_id = d.pop("tmdbId", UNSET)

    movie_collection_resource = cls(
      title=title,
      tmdb_id=tmdb_id,
    )

    return movie_collection_resource
