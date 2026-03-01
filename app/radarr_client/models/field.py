from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.privacy_level import PrivacyLevel
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.select_option import SelectOption


T = TypeVar("T", bound="Field")


@_attrs_define
class Field:
  """
  Attributes:
      order (int | Unset):
      name (None | str | Unset):
      label (None | str | Unset):
      unit (None | str | Unset):
      help_text (None | str | Unset):
      help_text_warning (None | str | Unset):
      help_link (None | str | Unset):
      value (Any | Unset):
      type_ (None | str | Unset):
      advanced (bool | Unset):
      select_options (list[SelectOption] | None | Unset):
      select_options_provider_action (None | str | Unset):
      section (None | str | Unset):
      hidden (None | str | Unset):
      privacy (PrivacyLevel | Unset):
      placeholder (None | str | Unset):
      is_float (bool | Unset):
  """

  order: int | Unset = UNSET
  name: None | str | Unset = UNSET
  label: None | str | Unset = UNSET
  unit: None | str | Unset = UNSET
  help_text: None | str | Unset = UNSET
  help_text_warning: None | str | Unset = UNSET
  help_link: None | str | Unset = UNSET
  value: Any | Unset = UNSET
  type_: None | str | Unset = UNSET
  advanced: bool | Unset = UNSET
  select_options: list[SelectOption] | None | Unset = UNSET
  select_options_provider_action: None | str | Unset = UNSET
  section: None | str | Unset = UNSET
  hidden: None | str | Unset = UNSET
  privacy: PrivacyLevel | Unset = UNSET
  placeholder: None | str | Unset = UNSET
  is_float: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    order = self.order

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    label: None | str | Unset
    if isinstance(self.label, Unset):
      label = UNSET
    else:
      label = self.label

    unit: None | str | Unset
    if isinstance(self.unit, Unset):
      unit = UNSET
    else:
      unit = self.unit

    help_text: None | str | Unset
    if isinstance(self.help_text, Unset):
      help_text = UNSET
    else:
      help_text = self.help_text

    help_text_warning: None | str | Unset
    if isinstance(self.help_text_warning, Unset):
      help_text_warning = UNSET
    else:
      help_text_warning = self.help_text_warning

    help_link: None | str | Unset
    if isinstance(self.help_link, Unset):
      help_link = UNSET
    else:
      help_link = self.help_link

    value = self.value

    type_: None | str | Unset
    if isinstance(self.type_, Unset):
      type_ = UNSET
    else:
      type_ = self.type_

    advanced = self.advanced

    select_options: list[dict[str, Any]] | None | Unset
    if isinstance(self.select_options, Unset):
      select_options = UNSET
    elif isinstance(self.select_options, list):
      select_options = []
      for select_options_type_0_item_data in self.select_options:
        select_options_type_0_item = select_options_type_0_item_data.to_dict()
        select_options.append(select_options_type_0_item)

    else:
      select_options = self.select_options

    select_options_provider_action: None | str | Unset
    if isinstance(self.select_options_provider_action, Unset):
      select_options_provider_action = UNSET
    else:
      select_options_provider_action = self.select_options_provider_action

    section: None | str | Unset
    if isinstance(self.section, Unset):
      section = UNSET
    else:
      section = self.section

    hidden: None | str | Unset
    if isinstance(self.hidden, Unset):
      hidden = UNSET
    else:
      hidden = self.hidden

    privacy: str | Unset = UNSET
    if not isinstance(self.privacy, Unset):
      privacy = self.privacy.value

    placeholder: None | str | Unset
    if isinstance(self.placeholder, Unset):
      placeholder = UNSET
    else:
      placeholder = self.placeholder

    is_float = self.is_float

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if order is not UNSET:
      field_dict["order"] = order
    if name is not UNSET:
      field_dict["name"] = name
    if label is not UNSET:
      field_dict["label"] = label
    if unit is not UNSET:
      field_dict["unit"] = unit
    if help_text is not UNSET:
      field_dict["helpText"] = help_text
    if help_text_warning is not UNSET:
      field_dict["helpTextWarning"] = help_text_warning
    if help_link is not UNSET:
      field_dict["helpLink"] = help_link
    if value is not UNSET:
      field_dict["value"] = value
    if type_ is not UNSET:
      field_dict["type"] = type_
    if advanced is not UNSET:
      field_dict["advanced"] = advanced
    if select_options is not UNSET:
      field_dict["selectOptions"] = select_options
    if select_options_provider_action is not UNSET:
      field_dict["selectOptionsProviderAction"] = select_options_provider_action
    if section is not UNSET:
      field_dict["section"] = section
    if hidden is not UNSET:
      field_dict["hidden"] = hidden
    if privacy is not UNSET:
      field_dict["privacy"] = privacy
    if placeholder is not UNSET:
      field_dict["placeholder"] = placeholder
    if is_float is not UNSET:
      field_dict["isFloat"] = is_float

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.select_option import SelectOption

    d = dict(src_dict)
    order = d.pop("order", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    def _parse_label(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    label = _parse_label(d.pop("label", UNSET))

    def _parse_unit(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    unit = _parse_unit(d.pop("unit", UNSET))

    def _parse_help_text(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    help_text = _parse_help_text(d.pop("helpText", UNSET))

    def _parse_help_text_warning(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    help_text_warning = _parse_help_text_warning(d.pop("helpTextWarning", UNSET))

    def _parse_help_link(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    help_link = _parse_help_link(d.pop("helpLink", UNSET))

    value = d.pop("value", UNSET)

    def _parse_type_(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    type_ = _parse_type_(d.pop("type", UNSET))

    advanced = d.pop("advanced", UNSET)

    def _parse_select_options(data: object) -> list[SelectOption] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        select_options_type_0 = []
        _select_options_type_0 = data
        for select_options_type_0_item_data in _select_options_type_0:
          select_options_type_0_item = SelectOption.from_dict(select_options_type_0_item_data)

          select_options_type_0.append(select_options_type_0_item)

        return select_options_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[SelectOption] | None | Unset, data)

    select_options = _parse_select_options(d.pop("selectOptions", UNSET))

    def _parse_select_options_provider_action(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    select_options_provider_action = _parse_select_options_provider_action(
      d.pop("selectOptionsProviderAction", UNSET)
    )

    def _parse_section(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    section = _parse_section(d.pop("section", UNSET))

    def _parse_hidden(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    hidden = _parse_hidden(d.pop("hidden", UNSET))

    _privacy = d.pop("privacy", UNSET)
    privacy: PrivacyLevel | Unset
    if isinstance(_privacy, Unset):
      privacy = UNSET
    else:
      privacy = PrivacyLevel(_privacy)

    def _parse_placeholder(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    placeholder = _parse_placeholder(d.pop("placeholder", UNSET))

    is_float = d.pop("isFloat", UNSET)

    field = cls(
      order=order,
      name=name,
      label=label,
      unit=unit,
      help_text=help_text,
      help_text_warning=help_text_warning,
      help_link=help_link,
      value=value,
      type_=type_,
      advanced=advanced,
      select_options=select_options,
      select_options_provider_action=select_options_provider_action,
      section=section,
      hidden=hidden,
      privacy=privacy,
      placeholder=placeholder,
      is_float=is_float,
    )

    return field
