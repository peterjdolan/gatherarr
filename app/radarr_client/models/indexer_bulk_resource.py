from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexerBulkResource")


@_attrs_define
class IndexerBulkResource:
  """
  Attributes:
      ids (list[int] | None | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      enable_rss (bool | None | Unset):
      enable_automatic_search (bool | None | Unset):
      enable_interactive_search (bool | None | Unset):
      priority (int | None | Unset):
  """

  ids: list[int] | None | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  enable_rss: bool | None | Unset = UNSET
  enable_automatic_search: bool | None | Unset = UNSET
  enable_interactive_search: bool | None | Unset = UNSET
  priority: int | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    ids: list[int] | None | Unset
    if isinstance(self.ids, Unset):
      ids = UNSET
    elif isinstance(self.ids, list):
      ids = self.ids

    else:
      ids = self.ids

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    apply_tags: str | Unset = UNSET
    if not isinstance(self.apply_tags, Unset):
      apply_tags = self.apply_tags.value

    enable_rss: bool | None | Unset
    if isinstance(self.enable_rss, Unset):
      enable_rss = UNSET
    else:
      enable_rss = self.enable_rss

    enable_automatic_search: bool | None | Unset
    if isinstance(self.enable_automatic_search, Unset):
      enable_automatic_search = UNSET
    else:
      enable_automatic_search = self.enable_automatic_search

    enable_interactive_search: bool | None | Unset
    if isinstance(self.enable_interactive_search, Unset):
      enable_interactive_search = UNSET
    else:
      enable_interactive_search = self.enable_interactive_search

    priority: int | None | Unset
    if isinstance(self.priority, Unset):
      priority = UNSET
    else:
      priority = self.priority

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if ids is not UNSET:
      field_dict["ids"] = ids
    if tags is not UNSET:
      field_dict["tags"] = tags
    if apply_tags is not UNSET:
      field_dict["applyTags"] = apply_tags
    if enable_rss is not UNSET:
      field_dict["enableRss"] = enable_rss
    if enable_automatic_search is not UNSET:
      field_dict["enableAutomaticSearch"] = enable_automatic_search
    if enable_interactive_search is not UNSET:
      field_dict["enableInteractiveSearch"] = enable_interactive_search
    if priority is not UNSET:
      field_dict["priority"] = priority

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_ids(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        ids_type_0 = cast(list[int], data)

        return ids_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    ids = _parse_ids(d.pop("ids", UNSET))

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

    _apply_tags = d.pop("applyTags", UNSET)
    apply_tags: ApplyTags | Unset
    if isinstance(_apply_tags, Unset):
      apply_tags = UNSET
    else:
      apply_tags = ApplyTags(_apply_tags)

    def _parse_enable_rss(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable_rss = _parse_enable_rss(d.pop("enableRss", UNSET))

    def _parse_enable_automatic_search(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable_automatic_search = _parse_enable_automatic_search(d.pop("enableAutomaticSearch", UNSET))

    def _parse_enable_interactive_search(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable_interactive_search = _parse_enable_interactive_search(
      d.pop("enableInteractiveSearch", UNSET)
    )

    def _parse_priority(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    priority = _parse_priority(d.pop("priority", UNSET))

    indexer_bulk_resource = cls(
      ids=ids,
      tags=tags,
      apply_tags=apply_tags,
      enable_rss=enable_rss,
      enable_automatic_search=enable_automatic_search,
      enable_interactive_search=enable_interactive_search,
      priority=priority,
    )

    return indexer_bulk_resource
