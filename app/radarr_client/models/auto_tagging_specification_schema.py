from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.field import Field


T = TypeVar("T", bound="AutoTaggingSpecificationSchema")


@_attrs_define
class AutoTaggingSpecificationSchema:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      implementation (None | str | Unset):
      implementation_name (None | str | Unset):
      negate (bool | Unset):
      required (bool | Unset):
      fields (list[Field] | None | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  implementation: None | str | Unset = UNSET
  implementation_name: None | str | Unset = UNSET
  negate: bool | Unset = UNSET
  required: bool | Unset = UNSET
  fields: list[Field] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    implementation: None | str | Unset
    if isinstance(self.implementation, Unset):
      implementation = UNSET
    else:
      implementation = self.implementation

    implementation_name: None | str | Unset
    if isinstance(self.implementation_name, Unset):
      implementation_name = UNSET
    else:
      implementation_name = self.implementation_name

    negate = self.negate

    required = self.required

    fields: list[dict[str, Any]] | None | Unset
    if isinstance(self.fields, Unset):
      fields = UNSET
    elif isinstance(self.fields, list):
      fields = []
      for fields_type_0_item_data in self.fields:
        fields_type_0_item = fields_type_0_item_data.to_dict()
        fields.append(fields_type_0_item)

    else:
      fields = self.fields

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if implementation is not UNSET:
      field_dict["implementation"] = implementation
    if implementation_name is not UNSET:
      field_dict["implementationName"] = implementation_name
    if negate is not UNSET:
      field_dict["negate"] = negate
    if required is not UNSET:
      field_dict["required"] = required
    if fields is not UNSET:
      field_dict["fields"] = fields

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.field import Field

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    def _parse_implementation(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    implementation = _parse_implementation(d.pop("implementation", UNSET))

    def _parse_implementation_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    implementation_name = _parse_implementation_name(d.pop("implementationName", UNSET))

    negate = d.pop("negate", UNSET)

    required = d.pop("required", UNSET)

    def _parse_fields(data: object) -> list[Field] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        fields_type_0 = []
        _fields_type_0 = data
        for fields_type_0_item_data in _fields_type_0:
          fields_type_0_item = Field.from_dict(fields_type_0_item_data)

          fields_type_0.append(fields_type_0_item)

        return fields_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[Field] | None | Unset, data)

    fields = _parse_fields(d.pop("fields", UNSET))

    auto_tagging_specification_schema = cls(
      id=id,
      name=name,
      implementation=implementation,
      implementation_name=implementation_name,
      negate=negate,
      required=required,
      fields=fields,
    )

    return auto_tagging_specification_schema
