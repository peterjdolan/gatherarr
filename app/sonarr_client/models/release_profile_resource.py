from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReleaseProfileResource")


@_attrs_define
class ReleaseProfileResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      enabled (bool | Unset):
      required (Any | Unset):
      ignored (Any | Unset):
      indexer_id (int | Unset):
      tags (list[int] | None | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  enabled: bool | Unset = UNSET
  required: Any | Unset = UNSET
  ignored: Any | Unset = UNSET
  indexer_id: int | Unset = UNSET
  tags: list[int] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    enabled = self.enabled

    required = self.required

    ignored = self.ignored

    indexer_id = self.indexer_id

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if enabled is not UNSET:
      field_dict["enabled"] = enabled
    if required is not UNSET:
      field_dict["required"] = required
    if ignored is not UNSET:
      field_dict["ignored"] = ignored
    if indexer_id is not UNSET:
      field_dict["indexerId"] = indexer_id
    if tags is not UNSET:
      field_dict["tags"] = tags

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    enabled = d.pop("enabled", UNSET)

    required = d.pop("required", UNSET)

    ignored = d.pop("ignored", UNSET)

    indexer_id = d.pop("indexerId", UNSET)

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

    release_profile_resource = cls(
      id=id,
      name=name,
      enabled=enabled,
      required=required,
      ignored=ignored,
      indexer_id=indexer_id,
      tags=tags,
    )

    return release_profile_resource
