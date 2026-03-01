from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.update_changes import UpdateChanges


T = TypeVar("T", bound="UpdateResource")


@_attrs_define
class UpdateResource:
  """
  Attributes:
      id (int | Unset):
      version (None | str | Unset):
      branch (None | str | Unset):
      release_date (datetime.datetime | Unset):
      file_name (None | str | Unset):
      url (None | str | Unset):
      installed (bool | Unset):
      installed_on (datetime.datetime | None | Unset):
      installable (bool | Unset):
      latest (bool | Unset):
      changes (UpdateChanges | Unset):
      hash_ (None | str | Unset):
  """

  id: int | Unset = UNSET
  version: None | str | Unset = UNSET
  branch: None | str | Unset = UNSET
  release_date: datetime.datetime | Unset = UNSET
  file_name: None | str | Unset = UNSET
  url: None | str | Unset = UNSET
  installed: bool | Unset = UNSET
  installed_on: datetime.datetime | None | Unset = UNSET
  installable: bool | Unset = UNSET
  latest: bool | Unset = UNSET
  changes: UpdateChanges | Unset = UNSET
  hash_: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    version: None | str | Unset
    if isinstance(self.version, Unset):
      version = UNSET
    else:
      version = self.version

    branch: None | str | Unset
    if isinstance(self.branch, Unset):
      branch = UNSET
    else:
      branch = self.branch

    release_date: str | Unset = UNSET
    if not isinstance(self.release_date, Unset):
      release_date = self.release_date.isoformat()

    file_name: None | str | Unset
    if isinstance(self.file_name, Unset):
      file_name = UNSET
    else:
      file_name = self.file_name

    url: None | str | Unset
    if isinstance(self.url, Unset):
      url = UNSET
    else:
      url = self.url

    installed = self.installed

    installed_on: None | str | Unset
    if isinstance(self.installed_on, Unset):
      installed_on = UNSET
    elif isinstance(self.installed_on, datetime.datetime):
      installed_on = self.installed_on.isoformat()
    else:
      installed_on = self.installed_on

    installable = self.installable

    latest = self.latest

    changes: dict[str, Any] | Unset = UNSET
    if not isinstance(self.changes, Unset):
      changes = self.changes.to_dict()

    hash_: None | str | Unset
    if isinstance(self.hash_, Unset):
      hash_ = UNSET
    else:
      hash_ = self.hash_

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if version is not UNSET:
      field_dict["version"] = version
    if branch is not UNSET:
      field_dict["branch"] = branch
    if release_date is not UNSET:
      field_dict["releaseDate"] = release_date
    if file_name is not UNSET:
      field_dict["fileName"] = file_name
    if url is not UNSET:
      field_dict["url"] = url
    if installed is not UNSET:
      field_dict["installed"] = installed
    if installed_on is not UNSET:
      field_dict["installedOn"] = installed_on
    if installable is not UNSET:
      field_dict["installable"] = installable
    if latest is not UNSET:
      field_dict["latest"] = latest
    if changes is not UNSET:
      field_dict["changes"] = changes
    if hash_ is not UNSET:
      field_dict["hash"] = hash_

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.update_changes import UpdateChanges

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    version = _parse_version(d.pop("version", UNSET))

    def _parse_branch(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    branch = _parse_branch(d.pop("branch", UNSET))

    _release_date = d.pop("releaseDate", UNSET)
    release_date: datetime.datetime | Unset
    if isinstance(_release_date, Unset):
      release_date = UNSET
    else:
      release_date = isoparse(_release_date)

    def _parse_file_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    file_name = _parse_file_name(d.pop("fileName", UNSET))

    def _parse_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    url = _parse_url(d.pop("url", UNSET))

    installed = d.pop("installed", UNSET)

    def _parse_installed_on(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        installed_on_type_0 = isoparse(data)

        return installed_on_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    installed_on = _parse_installed_on(d.pop("installedOn", UNSET))

    installable = d.pop("installable", UNSET)

    latest = d.pop("latest", UNSET)

    _changes = d.pop("changes", UNSET)
    changes: UpdateChanges | Unset
    if isinstance(_changes, Unset):
      changes = UNSET
    else:
      changes = UpdateChanges.from_dict(_changes)

    def _parse_hash_(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    hash_ = _parse_hash_(d.pop("hash", UNSET))

    update_resource = cls(
      id=id,
      version=version,
      branch=branch,
      release_date=release_date,
      file_name=file_name,
      url=url,
      installed=installed,
      installed_on=installed_on,
      installable=installable,
      latest=latest,
      changes=changes,
      hash_=hash_,
    )

    return update_resource
