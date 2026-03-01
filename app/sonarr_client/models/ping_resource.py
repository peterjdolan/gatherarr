from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="PingResource")


@_attrs_define
class PingResource:
  """
  Attributes:
      status (None | str | Unset):
  """

  status: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    status: None | str | Unset
    if isinstance(self.status, Unset):
      status = UNSET
    else:
      status = self.status

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if status is not UNSET:
      field_dict["status"] = status

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_status(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    status = _parse_status(d.pop("status", UNSET))

    ping_resource = cls(
      status=status,
    )

    return ping_resource
