from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrackedDownloadStatusMessage")


@_attrs_define
class TrackedDownloadStatusMessage:
  """
  Attributes:
      title (None | str | Unset):
      messages (list[str] | None | Unset):
  """

  title: None | str | Unset = UNSET
  messages: list[str] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    messages: list[str] | None | Unset
    if isinstance(self.messages, Unset):
      messages = UNSET
    elif isinstance(self.messages, list):
      messages = self.messages

    else:
      messages = self.messages

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if title is not UNSET:
      field_dict["title"] = title
    if messages is not UNSET:
      field_dict["messages"] = messages

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    def _parse_messages(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        messages_type_0 = cast(list[str], data)

        return messages_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    messages = _parse_messages(d.pop("messages", UNSET))

    tracked_download_status_message = cls(
      title=title,
      messages=messages,
    )

    return tracked_download_status_message
