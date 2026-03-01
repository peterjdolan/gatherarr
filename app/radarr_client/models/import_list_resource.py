from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.import_list_type import ImportListType
from ..models.monitor_types import MonitorTypes
from ..models.movie_status_type import MovieStatusType
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.field import Field
  from ..models.provider_message import ProviderMessage


T = TypeVar("T", bound="ImportListResource")


@_attrs_define
class ImportListResource:
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
      presets (list[ImportListResource] | None | Unset):
      enabled (bool | Unset):
      enable_auto (bool | Unset):
      monitor (MonitorTypes | Unset):
      root_folder_path (None | str | Unset):
      quality_profile_id (int | Unset):
      search_on_add (bool | Unset):
      minimum_availability (MovieStatusType | Unset):
      list_type (ImportListType | Unset):
      list_order (int | Unset):
      min_refresh_interval (str | Unset):
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
  presets: list[ImportListResource] | None | Unset = UNSET
  enabled: bool | Unset = UNSET
  enable_auto: bool | Unset = UNSET
  monitor: MonitorTypes | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  quality_profile_id: int | Unset = UNSET
  search_on_add: bool | Unset = UNSET
  minimum_availability: MovieStatusType | Unset = UNSET
  list_type: ImportListType | Unset = UNSET
  list_order: int | Unset = UNSET
  min_refresh_interval: str | Unset = UNSET

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

    enabled = self.enabled

    enable_auto = self.enable_auto

    monitor: str | Unset = UNSET
    if not isinstance(self.monitor, Unset):
      monitor = self.monitor.value

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

    quality_profile_id = self.quality_profile_id

    search_on_add = self.search_on_add

    minimum_availability: str | Unset = UNSET
    if not isinstance(self.minimum_availability, Unset):
      minimum_availability = self.minimum_availability.value

    list_type: str | Unset = UNSET
    if not isinstance(self.list_type, Unset):
      list_type = self.list_type.value

    list_order = self.list_order

    min_refresh_interval = self.min_refresh_interval

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
    if enabled is not UNSET:
      field_dict["enabled"] = enabled
    if enable_auto is not UNSET:
      field_dict["enableAuto"] = enable_auto
    if monitor is not UNSET:
      field_dict["monitor"] = monitor
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if search_on_add is not UNSET:
      field_dict["searchOnAdd"] = search_on_add
    if minimum_availability is not UNSET:
      field_dict["minimumAvailability"] = minimum_availability
    if list_type is not UNSET:
      field_dict["listType"] = list_type
    if list_order is not UNSET:
      field_dict["listOrder"] = list_order
    if min_refresh_interval is not UNSET:
      field_dict["minRefreshInterval"] = min_refresh_interval

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

    def _parse_presets(data: object) -> list[ImportListResource] | None | Unset:
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
          presets_type_0_item = ImportListResource.from_dict(presets_type_0_item_data)

          presets_type_0.append(presets_type_0_item)

        return presets_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[ImportListResource] | None | Unset, data)

    presets = _parse_presets(d.pop("presets", UNSET))

    enabled = d.pop("enabled", UNSET)

    enable_auto = d.pop("enableAuto", UNSET)

    _monitor = d.pop("monitor", UNSET)
    monitor: MonitorTypes | Unset
    if isinstance(_monitor, Unset):
      monitor = UNSET
    else:
      monitor = MonitorTypes(_monitor)

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

    quality_profile_id = d.pop("qualityProfileId", UNSET)

    search_on_add = d.pop("searchOnAdd", UNSET)

    _minimum_availability = d.pop("minimumAvailability", UNSET)
    minimum_availability: MovieStatusType | Unset
    if isinstance(_minimum_availability, Unset):
      minimum_availability = UNSET
    else:
      minimum_availability = MovieStatusType(_minimum_availability)

    _list_type = d.pop("listType", UNSET)
    list_type: ImportListType | Unset
    if isinstance(_list_type, Unset):
      list_type = UNSET
    else:
      list_type = ImportListType(_list_type)

    list_order = d.pop("listOrder", UNSET)

    min_refresh_interval = d.pop("minRefreshInterval", UNSET)

    import_list_resource = cls(
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
      enabled=enabled,
      enable_auto=enable_auto,
      monitor=monitor,
      root_folder_path=root_folder_path,
      quality_profile_id=quality_profile_id,
      search_on_add=search_on_add,
      minimum_availability=minimum_availability,
      list_type=list_type,
      list_order=list_order,
      min_refresh_interval=min_refresh_interval,
    )

    return import_list_resource
