from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.credit_type import CreditType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.media_cover import MediaCover


T = TypeVar("T", bound="CreditResource")


@_attrs_define
class CreditResource:
  """
  Attributes:
      id (int | Unset):
      person_name (None | str | Unset):
      credit_tmdb_id (None | str | Unset):
      person_tmdb_id (int | Unset):
      movie_metadata_id (int | Unset):
      images (list[MediaCover] | None | Unset):
      department (None | str | Unset):
      job (None | str | Unset):
      character (None | str | Unset):
      order (int | Unset):
      type_ (CreditType | Unset):
  """

  id: int | Unset = UNSET
  person_name: None | str | Unset = UNSET
  credit_tmdb_id: None | str | Unset = UNSET
  person_tmdb_id: int | Unset = UNSET
  movie_metadata_id: int | Unset = UNSET
  images: list[MediaCover] | None | Unset = UNSET
  department: None | str | Unset = UNSET
  job: None | str | Unset = UNSET
  character: None | str | Unset = UNSET
  order: int | Unset = UNSET
  type_: CreditType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    person_name: None | str | Unset
    if isinstance(self.person_name, Unset):
      person_name = UNSET
    else:
      person_name = self.person_name

    credit_tmdb_id: None | str | Unset
    if isinstance(self.credit_tmdb_id, Unset):
      credit_tmdb_id = UNSET
    else:
      credit_tmdb_id = self.credit_tmdb_id

    person_tmdb_id = self.person_tmdb_id

    movie_metadata_id = self.movie_metadata_id

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

    department: None | str | Unset
    if isinstance(self.department, Unset):
      department = UNSET
    else:
      department = self.department

    job: None | str | Unset
    if isinstance(self.job, Unset):
      job = UNSET
    else:
      job = self.job

    character: None | str | Unset
    if isinstance(self.character, Unset):
      character = UNSET
    else:
      character = self.character

    order = self.order

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if person_name is not UNSET:
      field_dict["personName"] = person_name
    if credit_tmdb_id is not UNSET:
      field_dict["creditTmdbId"] = credit_tmdb_id
    if person_tmdb_id is not UNSET:
      field_dict["personTmdbId"] = person_tmdb_id
    if movie_metadata_id is not UNSET:
      field_dict["movieMetadataId"] = movie_metadata_id
    if images is not UNSET:
      field_dict["images"] = images
    if department is not UNSET:
      field_dict["department"] = department
    if job is not UNSET:
      field_dict["job"] = job
    if character is not UNSET:
      field_dict["character"] = character
    if order is not UNSET:
      field_dict["order"] = order
    if type_ is not UNSET:
      field_dict["type"] = type_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.media_cover import MediaCover

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_person_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    person_name = _parse_person_name(d.pop("personName", UNSET))

    def _parse_credit_tmdb_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    credit_tmdb_id = _parse_credit_tmdb_id(d.pop("creditTmdbId", UNSET))

    person_tmdb_id = d.pop("personTmdbId", UNSET)

    movie_metadata_id = d.pop("movieMetadataId", UNSET)

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

    def _parse_department(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    department = _parse_department(d.pop("department", UNSET))

    def _parse_job(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    job = _parse_job(d.pop("job", UNSET))

    def _parse_character(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    character = _parse_character(d.pop("character", UNSET))

    order = d.pop("order", UNSET)

    _type_ = d.pop("type", UNSET)
    type_: CreditType | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = CreditType(_type_)

    credit_resource = cls(
      id=id,
      person_name=person_name,
      credit_tmdb_id=credit_tmdb_id,
      person_tmdb_id=person_tmdb_id,
      movie_metadata_id=movie_metadata_id,
      images=images,
      department=department,
      job=job,
      character=character,
      order=order,
      type_=type_,
    )

    return credit_resource
