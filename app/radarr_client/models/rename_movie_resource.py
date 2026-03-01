from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RenameMovieResource")


@_attrs_define
class RenameMovieResource:
  """
  Attributes:
      id (int | Unset):
      movie_id (int | Unset):
      movie_file_id (int | Unset):
      existing_path (None | str | Unset):
      new_path (None | str | Unset):
  """

  id: int | Unset = UNSET
  movie_id: int | Unset = UNSET
  movie_file_id: int | Unset = UNSET
  existing_path: None | str | Unset = UNSET
  new_path: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    movie_id = self.movie_id

    movie_file_id = self.movie_file_id

    existing_path: None | str | Unset
    if isinstance(self.existing_path, Unset):
      existing_path = UNSET
    else:
      existing_path = self.existing_path

    new_path: None | str | Unset
    if isinstance(self.new_path, Unset):
      new_path = UNSET
    else:
      new_path = self.new_path

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if movie_id is not UNSET:
      field_dict["movieId"] = movie_id
    if movie_file_id is not UNSET:
      field_dict["movieFileId"] = movie_file_id
    if existing_path is not UNSET:
      field_dict["existingPath"] = existing_path
    if new_path is not UNSET:
      field_dict["newPath"] = new_path

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    movie_id = d.pop("movieId", UNSET)

    movie_file_id = d.pop("movieFileId", UNSET)

    def _parse_existing_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    existing_path = _parse_existing_path(d.pop("existingPath", UNSET))

    def _parse_new_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    new_path = _parse_new_path(d.pop("newPath", UNSET))

    rename_movie_resource = cls(
      id=id,
      movie_id=movie_id,
      movie_file_id=movie_file_id,
      existing_path=existing_path,
      new_path=new_path,
    )

    return rename_movie_resource
