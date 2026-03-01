from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.sort_direction import SortDirection
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.episode_resource import EpisodeResource


T = TypeVar("T", bound="EpisodeResourcePagingResource")


@_attrs_define
class EpisodeResourcePagingResource:
  """
  Attributes:
      page (int | Unset):
      page_size (int | Unset):
      sort_key (None | str | Unset):
      sort_direction (SortDirection | Unset):
      total_records (int | Unset):
      records (list[EpisodeResource] | None | Unset):
  """

  page: int | Unset = UNSET
  page_size: int | Unset = UNSET
  sort_key: None | str | Unset = UNSET
  sort_direction: SortDirection | Unset = UNSET
  total_records: int | Unset = UNSET
  records: list[EpisodeResource] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    page = self.page

    page_size = self.page_size

    sort_key: None | str | Unset
    if isinstance(self.sort_key, Unset):
      sort_key = UNSET
    else:
      sort_key = self.sort_key

    sort_direction: str | Unset = UNSET
    if not isinstance(self.sort_direction, Unset):
      sort_direction = self.sort_direction.value

    total_records = self.total_records

    records: list[dict[str, Any]] | None | Unset
    if isinstance(self.records, Unset):
      records = UNSET
    elif isinstance(self.records, list):
      records = []
      for records_type_0_item_data in self.records:
        records_type_0_item = records_type_0_item_data.to_dict()
        records.append(records_type_0_item)

    else:
      records = self.records

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if page is not UNSET:
      field_dict["page"] = page
    if page_size is not UNSET:
      field_dict["pageSize"] = page_size
    if sort_key is not UNSET:
      field_dict["sortKey"] = sort_key
    if sort_direction is not UNSET:
      field_dict["sortDirection"] = sort_direction
    if total_records is not UNSET:
      field_dict["totalRecords"] = total_records
    if records is not UNSET:
      field_dict["records"] = records

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.episode_resource import EpisodeResource

    d = dict(src_dict)
    page = d.pop("page", UNSET)

    page_size = d.pop("pageSize", UNSET)

    def _parse_sort_key(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sort_key = _parse_sort_key(d.pop("sortKey", UNSET))

    _sort_direction = d.pop("sortDirection", UNSET)
    sort_direction: SortDirection | Unset
    if isinstance(_sort_direction, Unset):
      sort_direction = UNSET
    else:
      sort_direction = SortDirection(_sort_direction)

    total_records = d.pop("totalRecords", UNSET)

    def _parse_records(data: object) -> list[EpisodeResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        records_type_0 = []
        _records_type_0 = data
        for records_type_0_item_data in _records_type_0:
          records_type_0_item = EpisodeResource.from_dict(records_type_0_item_data)

          records_type_0.append(records_type_0_item)

        return records_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[EpisodeResource] | None | Unset, data)

    records = _parse_records(d.pop("records", UNSET))

    episode_resource_paging_resource = cls(
      page=page,
      page_size=page_size,
      sort_key=sort_key,
      sort_direction=sort_direction,
      total_records=total_records,
      records=records,
    )

    return episode_resource_paging_resource
