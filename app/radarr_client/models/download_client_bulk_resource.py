from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.apply_tags import ApplyTags
from ..types import UNSET, Unset

T = TypeVar("T", bound="DownloadClientBulkResource")


@_attrs_define
class DownloadClientBulkResource:
  """
  Attributes:
      ids (list[int] | None | Unset):
      tags (list[int] | None | Unset):
      apply_tags (ApplyTags | Unset):
      enable (bool | None | Unset):
      priority (int | None | Unset):
      remove_completed_downloads (bool | None | Unset):
      remove_failed_downloads (bool | None | Unset):
  """

  ids: list[int] | None | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  apply_tags: ApplyTags | Unset = UNSET
  enable: bool | None | Unset = UNSET
  priority: int | None | Unset = UNSET
  remove_completed_downloads: bool | None | Unset = UNSET
  remove_failed_downloads: bool | None | Unset = UNSET

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

    enable: bool | None | Unset
    if isinstance(self.enable, Unset):
      enable = UNSET
    else:
      enable = self.enable

    priority: int | None | Unset
    if isinstance(self.priority, Unset):
      priority = UNSET
    else:
      priority = self.priority

    remove_completed_downloads: bool | None | Unset
    if isinstance(self.remove_completed_downloads, Unset):
      remove_completed_downloads = UNSET
    else:
      remove_completed_downloads = self.remove_completed_downloads

    remove_failed_downloads: bool | None | Unset
    if isinstance(self.remove_failed_downloads, Unset):
      remove_failed_downloads = UNSET
    else:
      remove_failed_downloads = self.remove_failed_downloads

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if ids is not UNSET:
      field_dict["ids"] = ids
    if tags is not UNSET:
      field_dict["tags"] = tags
    if apply_tags is not UNSET:
      field_dict["applyTags"] = apply_tags
    if enable is not UNSET:
      field_dict["enable"] = enable
    if priority is not UNSET:
      field_dict["priority"] = priority
    if remove_completed_downloads is not UNSET:
      field_dict["removeCompletedDownloads"] = remove_completed_downloads
    if remove_failed_downloads is not UNSET:
      field_dict["removeFailedDownloads"] = remove_failed_downloads

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

    def _parse_enable(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    enable = _parse_enable(d.pop("enable", UNSET))

    def _parse_priority(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    priority = _parse_priority(d.pop("priority", UNSET))

    def _parse_remove_completed_downloads(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    remove_completed_downloads = _parse_remove_completed_downloads(
      d.pop("removeCompletedDownloads", UNSET)
    )

    def _parse_remove_failed_downloads(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    remove_failed_downloads = _parse_remove_failed_downloads(d.pop("removeFailedDownloads", UNSET))

    download_client_bulk_resource = cls(
      ids=ids,
      tags=tags,
      apply_tags=apply_tags,
      enable=enable,
      priority=priority,
      remove_completed_downloads=remove_completed_downloads,
      remove_failed_downloads=remove_failed_downloads,
    )

    return download_client_bulk_resource
