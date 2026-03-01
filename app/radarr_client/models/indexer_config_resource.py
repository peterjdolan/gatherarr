from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexerConfigResource")


@_attrs_define
class IndexerConfigResource:
  """
  Attributes:
      id (int | Unset):
      minimum_age (int | Unset):
      maximum_size (int | Unset):
      retention (int | Unset):
      rss_sync_interval (int | Unset):
      prefer_indexer_flags (bool | Unset):
      availability_delay (int | Unset):
      allow_hardcoded_subs (bool | Unset):
      whitelisted_hardcoded_subs (None | str | Unset):
  """

  id: int | Unset = UNSET
  minimum_age: int | Unset = UNSET
  maximum_size: int | Unset = UNSET
  retention: int | Unset = UNSET
  rss_sync_interval: int | Unset = UNSET
  prefer_indexer_flags: bool | Unset = UNSET
  availability_delay: int | Unset = UNSET
  allow_hardcoded_subs: bool | Unset = UNSET
  whitelisted_hardcoded_subs: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    minimum_age = self.minimum_age

    maximum_size = self.maximum_size

    retention = self.retention

    rss_sync_interval = self.rss_sync_interval

    prefer_indexer_flags = self.prefer_indexer_flags

    availability_delay = self.availability_delay

    allow_hardcoded_subs = self.allow_hardcoded_subs

    whitelisted_hardcoded_subs: None | str | Unset
    if isinstance(self.whitelisted_hardcoded_subs, Unset):
      whitelisted_hardcoded_subs = UNSET
    else:
      whitelisted_hardcoded_subs = self.whitelisted_hardcoded_subs

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if minimum_age is not UNSET:
      field_dict["minimumAge"] = minimum_age
    if maximum_size is not UNSET:
      field_dict["maximumSize"] = maximum_size
    if retention is not UNSET:
      field_dict["retention"] = retention
    if rss_sync_interval is not UNSET:
      field_dict["rssSyncInterval"] = rss_sync_interval
    if prefer_indexer_flags is not UNSET:
      field_dict["preferIndexerFlags"] = prefer_indexer_flags
    if availability_delay is not UNSET:
      field_dict["availabilityDelay"] = availability_delay
    if allow_hardcoded_subs is not UNSET:
      field_dict["allowHardcodedSubs"] = allow_hardcoded_subs
    if whitelisted_hardcoded_subs is not UNSET:
      field_dict["whitelistedHardcodedSubs"] = whitelisted_hardcoded_subs

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    minimum_age = d.pop("minimumAge", UNSET)

    maximum_size = d.pop("maximumSize", UNSET)

    retention = d.pop("retention", UNSET)

    rss_sync_interval = d.pop("rssSyncInterval", UNSET)

    prefer_indexer_flags = d.pop("preferIndexerFlags", UNSET)

    availability_delay = d.pop("availabilityDelay", UNSET)

    allow_hardcoded_subs = d.pop("allowHardcodedSubs", UNSET)

    def _parse_whitelisted_hardcoded_subs(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    whitelisted_hardcoded_subs = _parse_whitelisted_hardcoded_subs(
      d.pop("whitelistedHardcodedSubs", UNSET)
    )

    indexer_config_resource = cls(
      id=id,
      minimum_age=minimum_age,
      maximum_size=maximum_size,
      retention=retention,
      rss_sync_interval=rss_sync_interval,
      prefer_indexer_flags=prefer_indexer_flags,
      availability_delay=availability_delay,
      allow_hardcoded_subs=allow_hardcoded_subs,
      whitelisted_hardcoded_subs=whitelisted_hardcoded_subs,
    )

    return indexer_config_resource
