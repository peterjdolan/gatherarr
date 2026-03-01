from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.download_protocol import DownloadProtocol
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.field import Field
  from ..models.provider_message import ProviderMessage


T = TypeVar("T", bound="IndexerResource")


@_attrs_define
class IndexerResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      fields (list[Field] | None | Unset):
      implementation_name (None | str | Unset):
      implementation (None | str | Unset):
      config_contract (None | str | Unset):
      info_link (None | str | Unset):
      message (ProviderMessage | Unset):
      tags (list[int] | None | Unset):
      presets (list[IndexerResource] | None | Unset):
      enable_rss (bool | Unset):
      enable_automatic_search (bool | Unset):
      enable_interactive_search (bool | Unset):
      supports_rss (bool | Unset):
      supports_search (bool | Unset):
      protocol (DownloadProtocol | Unset):
      priority (int | Unset):
      season_search_maximum_single_episode_age (int | Unset):
      download_client_id (int | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  fields: list[Field] | None | Unset = UNSET
  implementation_name: None | str | Unset = UNSET
  implementation: None | str | Unset = UNSET
  config_contract: None | str | Unset = UNSET
  info_link: None | str | Unset = UNSET
  message: ProviderMessage | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  presets: list[IndexerResource] | None | Unset = UNSET
  enable_rss: bool | Unset = UNSET
  enable_automatic_search: bool | Unset = UNSET
  enable_interactive_search: bool | Unset = UNSET
  supports_rss: bool | Unset = UNSET
  supports_search: bool | Unset = UNSET
  protocol: DownloadProtocol | Unset = UNSET
  priority: int | Unset = UNSET
  season_search_maximum_single_episode_age: int | Unset = UNSET
  download_client_id: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

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

    implementation_name: None | str | Unset
    if isinstance(self.implementation_name, Unset):
      implementation_name = UNSET
    else:
      implementation_name = self.implementation_name

    implementation: None | str | Unset
    if isinstance(self.implementation, Unset):
      implementation = UNSET
    else:
      implementation = self.implementation

    config_contract: None | str | Unset
    if isinstance(self.config_contract, Unset):
      config_contract = UNSET
    else:
      config_contract = self.config_contract

    info_link: None | str | Unset
    if isinstance(self.info_link, Unset):
      info_link = UNSET
    else:
      info_link = self.info_link

    message: dict[str, Any] | Unset = UNSET
    if not isinstance(self.message, Unset):
      message = self.message.to_dict()

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    presets: list[dict[str, Any]] | None | Unset
    if isinstance(self.presets, Unset):
      presets = UNSET
    elif isinstance(self.presets, list):
      presets = []
      for presets_type_0_item_data in self.presets:
        presets_type_0_item = presets_type_0_item_data.to_dict()
        presets.append(presets_type_0_item)

    else:
      presets = self.presets

    enable_rss = self.enable_rss

    enable_automatic_search = self.enable_automatic_search

    enable_interactive_search = self.enable_interactive_search

    supports_rss = self.supports_rss

    supports_search = self.supports_search

    protocol: str | Unset = UNSET
    if not isinstance(self.protocol, Unset):
      protocol = self.protocol.value

    priority = self.priority

    season_search_maximum_single_episode_age = self.season_search_maximum_single_episode_age

    download_client_id = self.download_client_id

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if fields is not UNSET:
      field_dict["fields"] = fields
    if implementation_name is not UNSET:
      field_dict["implementationName"] = implementation_name
    if implementation is not UNSET:
      field_dict["implementation"] = implementation
    if config_contract is not UNSET:
      field_dict["configContract"] = config_contract
    if info_link is not UNSET:
      field_dict["infoLink"] = info_link
    if message is not UNSET:
      field_dict["message"] = message
    if tags is not UNSET:
      field_dict["tags"] = tags
    if presets is not UNSET:
      field_dict["presets"] = presets
    if enable_rss is not UNSET:
      field_dict["enableRss"] = enable_rss
    if enable_automatic_search is not UNSET:
      field_dict["enableAutomaticSearch"] = enable_automatic_search
    if enable_interactive_search is not UNSET:
      field_dict["enableInteractiveSearch"] = enable_interactive_search
    if supports_rss is not UNSET:
      field_dict["supportsRss"] = supports_rss
    if supports_search is not UNSET:
      field_dict["supportsSearch"] = supports_search
    if protocol is not UNSET:
      field_dict["protocol"] = protocol
    if priority is not UNSET:
      field_dict["priority"] = priority
    if season_search_maximum_single_episode_age is not UNSET:
      field_dict["seasonSearchMaximumSingleEpisodeAge"] = season_search_maximum_single_episode_age
    if download_client_id is not UNSET:
      field_dict["downloadClientId"] = download_client_id

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.field import Field
    from ..models.provider_message import ProviderMessage

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

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

    def _parse_implementation_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    implementation_name = _parse_implementation_name(d.pop("implementationName", UNSET))

    def _parse_implementation(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    implementation = _parse_implementation(d.pop("implementation", UNSET))

    def _parse_config_contract(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    config_contract = _parse_config_contract(d.pop("configContract", UNSET))

    def _parse_info_link(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    info_link = _parse_info_link(d.pop("infoLink", UNSET))

    _message = d.pop("message", UNSET)
    message: ProviderMessage | Unset
    if isinstance(_message, Unset):
      message = UNSET
    else:
      message = ProviderMessage.from_dict(_message)

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

    def _parse_presets(data: object) -> list[IndexerResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        presets_type_0 = []
        _presets_type_0 = data
        for presets_type_0_item_data in _presets_type_0:
          presets_type_0_item = IndexerResource.from_dict(presets_type_0_item_data)

          presets_type_0.append(presets_type_0_item)

        return presets_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[IndexerResource] | None | Unset, data)

    presets = _parse_presets(d.pop("presets", UNSET))

    enable_rss = d.pop("enableRss", UNSET)

    enable_automatic_search = d.pop("enableAutomaticSearch", UNSET)

    enable_interactive_search = d.pop("enableInteractiveSearch", UNSET)

    supports_rss = d.pop("supportsRss", UNSET)

    supports_search = d.pop("supportsSearch", UNSET)

    _protocol = d.pop("protocol", UNSET)
    protocol: DownloadProtocol | Unset
    if isinstance(_protocol, Unset):
      protocol = UNSET
    else:
      protocol = DownloadProtocol(_protocol)

    priority = d.pop("priority", UNSET)

    season_search_maximum_single_episode_age = d.pop("seasonSearchMaximumSingleEpisodeAge", UNSET)

    download_client_id = d.pop("downloadClientId", UNSET)

    indexer_resource = cls(
      id=id,
      name=name,
      fields=fields,
      implementation_name=implementation_name,
      implementation=implementation,
      config_contract=config_contract,
      info_link=info_link,
      message=message,
      tags=tags,
      presets=presets,
      enable_rss=enable_rss,
      enable_automatic_search=enable_automatic_search,
      enable_interactive_search=enable_interactive_search,
      supports_rss=supports_rss,
      supports_search=supports_search,
      protocol=protocol,
      priority=priority,
      season_search_maximum_single_episode_age=season_search_maximum_single_episode_age,
      download_client_id=download_client_id,
    )

    return indexer_resource
