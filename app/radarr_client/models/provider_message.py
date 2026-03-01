from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.provider_message_type import ProviderMessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderMessage")


@_attrs_define
class ProviderMessage:
  """
  Attributes:
      message (None | str | Unset):
      type_ (ProviderMessageType | Unset):
  """

  message: None | str | Unset = UNSET
  type_: ProviderMessageType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    message: None | str | Unset
    if isinstance(self.message, Unset):
      message = UNSET
    else:
      message = self.message

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if message is not UNSET:
      field_dict["message"] = message
    if type_ is not UNSET:
      field_dict["type"] = type_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    message = _parse_message(d.pop("message", UNSET))

    _type_ = d.pop("type", UNSET)
    type_: ProviderMessageType | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = ProviderMessageType(_type_)

    provider_message = cls(
      message=message,
      type_=type_,
    )

    return provider_message
