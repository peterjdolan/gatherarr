from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.quality import Quality


T = TypeVar("T", bound="QualityDefinitionResource")


@_attrs_define
class QualityDefinitionResource:
  """
  Attributes:
      id (int | Unset):
      quality (Quality | Unset):
      title (None | str | Unset):
      weight (int | Unset):
      min_size (float | None | Unset):
      max_size (float | None | Unset):
      preferred_size (float | None | Unset):
  """

  id: int | Unset = UNSET
  quality: Quality | Unset = UNSET
  title: None | str | Unset = UNSET
  weight: int | Unset = UNSET
  min_size: float | None | Unset = UNSET
  max_size: float | None | Unset = UNSET
  preferred_size: float | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    weight = self.weight

    min_size: float | None | Unset
    if isinstance(self.min_size, Unset):
      min_size = UNSET
    else:
      min_size = self.min_size

    max_size: float | None | Unset
    if isinstance(self.max_size, Unset):
      max_size = UNSET
    else:
      max_size = self.max_size

    preferred_size: float | None | Unset
    if isinstance(self.preferred_size, Unset):
      preferred_size = UNSET
    else:
      preferred_size = self.preferred_size

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if quality is not UNSET:
      field_dict["quality"] = quality
    if title is not UNSET:
      field_dict["title"] = title
    if weight is not UNSET:
      field_dict["weight"] = weight
    if min_size is not UNSET:
      field_dict["minSize"] = min_size
    if max_size is not UNSET:
      field_dict["maxSize"] = max_size
    if preferred_size is not UNSET:
      field_dict["preferredSize"] = preferred_size

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.quality import Quality

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    _quality = d.pop("quality", UNSET)
    quality: Quality | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = Quality.from_dict(_quality)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    weight = d.pop("weight", UNSET)

    def _parse_min_size(data: object) -> float | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(float | None | Unset, data)

    min_size = _parse_min_size(d.pop("minSize", UNSET))

    def _parse_max_size(data: object) -> float | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(float | None | Unset, data)

    max_size = _parse_max_size(d.pop("maxSize", UNSET))

    def _parse_preferred_size(data: object) -> float | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(float | None | Unset, data)

    preferred_size = _parse_preferred_size(d.pop("preferredSize", UNSET))

    quality_definition_resource = cls(
      id=id,
      quality=quality,
      title=title,
      weight=weight,
      min_size=min_size,
      max_size=max_size,
      preferred_size=preferred_size,
    )

    return quality_definition_resource
