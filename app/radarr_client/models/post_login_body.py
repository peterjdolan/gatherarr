from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostLoginBody")


@_attrs_define
class PostLoginBody:
  """
  Attributes:
      username (str | Unset):
      password (str | Unset):
      remember_me (str | Unset):
  """

  username: str | Unset = UNSET
  password: str | Unset = UNSET
  remember_me: str | Unset = UNSET
  additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

  def to_dict(self) -> dict[str, Any]:
    username = self.username

    password = self.password

    remember_me = self.remember_me

    field_dict: dict[str, Any] = {}
    field_dict.update(self.additional_properties)
    field_dict.update({})
    if username is not UNSET:
      field_dict["username"] = username
    if password is not UNSET:
      field_dict["password"] = password
    if remember_me is not UNSET:
      field_dict["rememberMe"] = remember_me

    return field_dict

  def to_multipart(self) -> types.RequestFiles:
    files: types.RequestFiles = []

    if not isinstance(self.username, Unset):
      files.append(("username", (None, str(self.username).encode(), "text/plain")))

    if not isinstance(self.password, Unset):
      files.append(("password", (None, str(self.password).encode(), "text/plain")))

    if not isinstance(self.remember_me, Unset):
      files.append(("rememberMe", (None, str(self.remember_me).encode(), "text/plain")))

    for prop_name, prop in self.additional_properties.items():
      files.append((prop_name, (None, str(prop).encode(), "text/plain")))

    return files

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    username = d.pop("username", UNSET)

    password = d.pop("password", UNSET)

    remember_me = d.pop("rememberMe", UNSET)

    post_login_body = cls(
      username=username,
      password=password,
      remember_me=remember_me,
    )

    post_login_body.additional_properties = d
    return post_login_body

  @property
  def additional_keys(self) -> list[str]:
    return list(self.additional_properties.keys())

  def __getitem__(self, key: str) -> Any:
    return self.additional_properties[key]

  def __setitem__(self, key: str, value: Any) -> None:
    self.additional_properties[key] = value

  def __delitem__(self, key: str) -> None:
    del self.additional_properties[key]

  def __contains__(self, key: str) -> bool:
    return key in self.additional_properties
