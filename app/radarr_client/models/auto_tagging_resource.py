from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.auto_tagging_specification_schema import AutoTaggingSpecificationSchema


T = TypeVar("T", bound="AutoTaggingResource")


@_attrs_define
class AutoTaggingResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      remove_tags_automatically (bool | Unset):
      tags (list[int] | None | Unset):
      specifications (list[AutoTaggingSpecificationSchema] | None | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  remove_tags_automatically: bool | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  specifications: list[AutoTaggingSpecificationSchema] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    remove_tags_automatically = self.remove_tags_automatically

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    specifications: list[dict[str, Any]] | None | Unset
    if isinstance(self.specifications, Unset):
      specifications = UNSET
    elif isinstance(self.specifications, list):
      specifications = []
      for specifications_type_0_item_data in self.specifications:
        specifications_type_0_item = specifications_type_0_item_data.to_dict()
        specifications.append(specifications_type_0_item)

    else:
      specifications = self.specifications

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if remove_tags_automatically is not UNSET:
      field_dict["removeTagsAutomatically"] = remove_tags_automatically
    if tags is not UNSET:
      field_dict["tags"] = tags
    if specifications is not UNSET:
      field_dict["specifications"] = specifications

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.auto_tagging_specification_schema import AutoTaggingSpecificationSchema

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    remove_tags_automatically = d.pop("removeTagsAutomatically", UNSET)

    def _parse_tags(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        tags_type_0 = cast(list[int], data)

        return tags_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    tags = _parse_tags(d.pop("tags", UNSET))

    def _parse_specifications(data: object) -> list[AutoTaggingSpecificationSchema] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        specifications_type_0 = []
        _specifications_type_0 = data
        for specifications_type_0_item_data in _specifications_type_0:
          specifications_type_0_item = AutoTaggingSpecificationSchema.from_dict(
            specifications_type_0_item_data
          )

          specifications_type_0.append(specifications_type_0_item)

        return specifications_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[AutoTaggingSpecificationSchema] | None | Unset, data)

    specifications = _parse_specifications(d.pop("specifications", UNSET))

    auto_tagging_resource = cls(
      id=id,
      name=name,
      remove_tags_automatically=remove_tags_automatically,
      tags=tags,
      specifications=specifications,
    )

    return auto_tagging_resource
