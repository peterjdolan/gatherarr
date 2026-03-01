from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.health_check_result import HealthCheckResult
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.http_uri import HttpUri


T = TypeVar("T", bound="HealthResource")


@_attrs_define
class HealthResource:
  """
  Attributes:
      id (int | Unset):
      source (None | str | Unset):
      type_ (HealthCheckResult | Unset):
      message (None | str | Unset):
      wiki_url (HttpUri | Unset):
  """

  id: int | Unset = UNSET
  source: None | str | Unset = UNSET
  type_: HealthCheckResult | Unset = UNSET
  message: None | str | Unset = UNSET
  wiki_url: HttpUri | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    source: None | str | Unset
    if isinstance(self.source, Unset):
      source = UNSET
    else:
      source = self.source

    type_: str | Unset = UNSET
    if not isinstance(self.type_, Unset):
      type_ = self.type_.value

    message: None | str | Unset
    if isinstance(self.message, Unset):
      message = UNSET
    else:
      message = self.message

    wiki_url: dict[str, Any] | Unset = UNSET
    if not isinstance(self.wiki_url, Unset):
      wiki_url = self.wiki_url.to_dict()

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if source is not UNSET:
      field_dict["source"] = source
    if type_ is not UNSET:
      field_dict["type"] = type_
    if message is not UNSET:
      field_dict["message"] = message
    if wiki_url is not UNSET:
      field_dict["wikiUrl"] = wiki_url

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.http_uri import HttpUri

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_source(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    source = _parse_source(d.pop("source", UNSET))

    _type_ = d.pop("type", UNSET)
    type_: HealthCheckResult | Unset
    if isinstance(_type_, Unset):
      type_ = UNSET
    else:
      type_ = HealthCheckResult(_type_)

    def _parse_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    message = _parse_message(d.pop("message", UNSET))

    _wiki_url = d.pop("wikiUrl", UNSET)
    wiki_url: HttpUri | Unset
    if isinstance(_wiki_url, Unset):
      wiki_url = UNSET
    else:
      wiki_url = HttpUri.from_dict(_wiki_url)

    health_resource = cls(
      id=id,
      source=source,
      type_=type_,
      message=message,
      wiki_url=wiki_url,
    )

    return health_resource
