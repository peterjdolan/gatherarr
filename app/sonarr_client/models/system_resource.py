from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.authentication_type import AuthenticationType
from ..models.database_type import DatabaseType
from ..models.runtime_mode import RuntimeMode
from ..models.update_mechanism import UpdateMechanism
from ..types import UNSET, Unset

T = TypeVar("T", bound="SystemResource")


@_attrs_define
class SystemResource:
  """
  Attributes:
      app_name (None | str | Unset):
      instance_name (None | str | Unset):
      version (None | str | Unset):
      build_time (datetime.datetime | Unset):
      is_debug (bool | Unset):
      is_production (bool | Unset):
      is_admin (bool | Unset):
      is_user_interactive (bool | Unset):
      startup_path (None | str | Unset):
      app_data (None | str | Unset):
      os_name (None | str | Unset):
      os_version (None | str | Unset):
      is_net_core (bool | Unset):
      is_linux (bool | Unset):
      is_osx (bool | Unset):
      is_windows (bool | Unset):
      is_docker (bool | Unset):
      mode (RuntimeMode | Unset):
      branch (None | str | Unset):
      authentication (AuthenticationType | Unset):
      sqlite_version (None | str | Unset):
      migration_version (int | Unset):
      url_base (None | str | Unset):
      runtime_version (None | str | Unset):
      runtime_name (None | str | Unset):
      start_time (datetime.datetime | Unset):
      package_version (None | str | Unset):
      package_author (None | str | Unset):
      package_update_mechanism (UpdateMechanism | Unset):
      package_update_mechanism_message (None | str | Unset):
      database_version (None | str | Unset):
      database_type (DatabaseType | Unset):
  """

  app_name: None | str | Unset = UNSET
  instance_name: None | str | Unset = UNSET
  version: None | str | Unset = UNSET
  build_time: datetime.datetime | Unset = UNSET
  is_debug: bool | Unset = UNSET
  is_production: bool | Unset = UNSET
  is_admin: bool | Unset = UNSET
  is_user_interactive: bool | Unset = UNSET
  startup_path: None | str | Unset = UNSET
  app_data: None | str | Unset = UNSET
  os_name: None | str | Unset = UNSET
  os_version: None | str | Unset = UNSET
  is_net_core: bool | Unset = UNSET
  is_linux: bool | Unset = UNSET
  is_osx: bool | Unset = UNSET
  is_windows: bool | Unset = UNSET
  is_docker: bool | Unset = UNSET
  mode: RuntimeMode | Unset = UNSET
  branch: None | str | Unset = UNSET
  authentication: AuthenticationType | Unset = UNSET
  sqlite_version: None | str | Unset = UNSET
  migration_version: int | Unset = UNSET
  url_base: None | str | Unset = UNSET
  runtime_version: None | str | Unset = UNSET
  runtime_name: None | str | Unset = UNSET
  start_time: datetime.datetime | Unset = UNSET
  package_version: None | str | Unset = UNSET
  package_author: None | str | Unset = UNSET
  package_update_mechanism: UpdateMechanism | Unset = UNSET
  package_update_mechanism_message: None | str | Unset = UNSET
  database_version: None | str | Unset = UNSET
  database_type: DatabaseType | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    app_name: None | str | Unset
    if isinstance(self.app_name, Unset):
      app_name = UNSET
    else:
      app_name = self.app_name

    instance_name: None | str | Unset
    if isinstance(self.instance_name, Unset):
      instance_name = UNSET
    else:
      instance_name = self.instance_name

    version: None | str | Unset
    if isinstance(self.version, Unset):
      version = UNSET
    else:
      version = self.version

    build_time: str | Unset = UNSET
    if not isinstance(self.build_time, Unset):
      build_time = self.build_time.isoformat()

    is_debug = self.is_debug

    is_production = self.is_production

    is_admin = self.is_admin

    is_user_interactive = self.is_user_interactive

    startup_path: None | str | Unset
    if isinstance(self.startup_path, Unset):
      startup_path = UNSET
    else:
      startup_path = self.startup_path

    app_data: None | str | Unset
    if isinstance(self.app_data, Unset):
      app_data = UNSET
    else:
      app_data = self.app_data

    os_name: None | str | Unset
    if isinstance(self.os_name, Unset):
      os_name = UNSET
    else:
      os_name = self.os_name

    os_version: None | str | Unset
    if isinstance(self.os_version, Unset):
      os_version = UNSET
    else:
      os_version = self.os_version

    is_net_core = self.is_net_core

    is_linux = self.is_linux

    is_osx = self.is_osx

    is_windows = self.is_windows

    is_docker = self.is_docker

    mode: str | Unset = UNSET
    if not isinstance(self.mode, Unset):
      mode = self.mode.value

    branch: None | str | Unset
    if isinstance(self.branch, Unset):
      branch = UNSET
    else:
      branch = self.branch

    authentication: str | Unset = UNSET
    if not isinstance(self.authentication, Unset):
      authentication = self.authentication.value

    sqlite_version: None | str | Unset
    if isinstance(self.sqlite_version, Unset):
      sqlite_version = UNSET
    else:
      sqlite_version = self.sqlite_version

    migration_version = self.migration_version

    url_base: None | str | Unset
    if isinstance(self.url_base, Unset):
      url_base = UNSET
    else:
      url_base = self.url_base

    runtime_version: None | str | Unset
    if isinstance(self.runtime_version, Unset):
      runtime_version = UNSET
    else:
      runtime_version = self.runtime_version

    runtime_name: None | str | Unset
    if isinstance(self.runtime_name, Unset):
      runtime_name = UNSET
    else:
      runtime_name = self.runtime_name

    start_time: str | Unset = UNSET
    if not isinstance(self.start_time, Unset):
      start_time = self.start_time.isoformat()

    package_version: None | str | Unset
    if isinstance(self.package_version, Unset):
      package_version = UNSET
    else:
      package_version = self.package_version

    package_author: None | str | Unset
    if isinstance(self.package_author, Unset):
      package_author = UNSET
    else:
      package_author = self.package_author

    package_update_mechanism: str | Unset = UNSET
    if not isinstance(self.package_update_mechanism, Unset):
      package_update_mechanism = self.package_update_mechanism.value

    package_update_mechanism_message: None | str | Unset
    if isinstance(self.package_update_mechanism_message, Unset):
      package_update_mechanism_message = UNSET
    else:
      package_update_mechanism_message = self.package_update_mechanism_message

    database_version: None | str | Unset
    if isinstance(self.database_version, Unset):
      database_version = UNSET
    else:
      database_version = self.database_version

    database_type: str | Unset = UNSET
    if not isinstance(self.database_type, Unset):
      database_type = self.database_type.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if app_name is not UNSET:
      field_dict["appName"] = app_name
    if instance_name is not UNSET:
      field_dict["instanceName"] = instance_name
    if version is not UNSET:
      field_dict["version"] = version
    if build_time is not UNSET:
      field_dict["buildTime"] = build_time
    if is_debug is not UNSET:
      field_dict["isDebug"] = is_debug
    if is_production is not UNSET:
      field_dict["isProduction"] = is_production
    if is_admin is not UNSET:
      field_dict["isAdmin"] = is_admin
    if is_user_interactive is not UNSET:
      field_dict["isUserInteractive"] = is_user_interactive
    if startup_path is not UNSET:
      field_dict["startupPath"] = startup_path
    if app_data is not UNSET:
      field_dict["appData"] = app_data
    if os_name is not UNSET:
      field_dict["osName"] = os_name
    if os_version is not UNSET:
      field_dict["osVersion"] = os_version
    if is_net_core is not UNSET:
      field_dict["isNetCore"] = is_net_core
    if is_linux is not UNSET:
      field_dict["isLinux"] = is_linux
    if is_osx is not UNSET:
      field_dict["isOsx"] = is_osx
    if is_windows is not UNSET:
      field_dict["isWindows"] = is_windows
    if is_docker is not UNSET:
      field_dict["isDocker"] = is_docker
    if mode is not UNSET:
      field_dict["mode"] = mode
    if branch is not UNSET:
      field_dict["branch"] = branch
    if authentication is not UNSET:
      field_dict["authentication"] = authentication
    if sqlite_version is not UNSET:
      field_dict["sqliteVersion"] = sqlite_version
    if migration_version is not UNSET:
      field_dict["migrationVersion"] = migration_version
    if url_base is not UNSET:
      field_dict["urlBase"] = url_base
    if runtime_version is not UNSET:
      field_dict["runtimeVersion"] = runtime_version
    if runtime_name is not UNSET:
      field_dict["runtimeName"] = runtime_name
    if start_time is not UNSET:
      field_dict["startTime"] = start_time
    if package_version is not UNSET:
      field_dict["packageVersion"] = package_version
    if package_author is not UNSET:
      field_dict["packageAuthor"] = package_author
    if package_update_mechanism is not UNSET:
      field_dict["packageUpdateMechanism"] = package_update_mechanism
    if package_update_mechanism_message is not UNSET:
      field_dict["packageUpdateMechanismMessage"] = package_update_mechanism_message
    if database_version is not UNSET:
      field_dict["databaseVersion"] = database_version
    if database_type is not UNSET:
      field_dict["databaseType"] = database_type

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)

    def _parse_app_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    app_name = _parse_app_name(d.pop("appName", UNSET))

    def _parse_instance_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    instance_name = _parse_instance_name(d.pop("instanceName", UNSET))

    def _parse_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    version = _parse_version(d.pop("version", UNSET))

    _build_time = d.pop("buildTime", UNSET)
    build_time: datetime.datetime | Unset
    if isinstance(_build_time, Unset):
      build_time = UNSET
    else:
      build_time = isoparse(_build_time)

    is_debug = d.pop("isDebug", UNSET)

    is_production = d.pop("isProduction", UNSET)

    is_admin = d.pop("isAdmin", UNSET)

    is_user_interactive = d.pop("isUserInteractive", UNSET)

    def _parse_startup_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    startup_path = _parse_startup_path(d.pop("startupPath", UNSET))

    def _parse_app_data(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    app_data = _parse_app_data(d.pop("appData", UNSET))

    def _parse_os_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    os_name = _parse_os_name(d.pop("osName", UNSET))

    def _parse_os_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    os_version = _parse_os_version(d.pop("osVersion", UNSET))

    is_net_core = d.pop("isNetCore", UNSET)

    is_linux = d.pop("isLinux", UNSET)

    is_osx = d.pop("isOsx", UNSET)

    is_windows = d.pop("isWindows", UNSET)

    is_docker = d.pop("isDocker", UNSET)

    _mode = d.pop("mode", UNSET)
    mode: RuntimeMode | Unset
    if isinstance(_mode, Unset):
      mode = UNSET
    else:
      mode = RuntimeMode(_mode)

    def _parse_branch(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    branch = _parse_branch(d.pop("branch", UNSET))

    _authentication = d.pop("authentication", UNSET)
    authentication: AuthenticationType | Unset
    if isinstance(_authentication, Unset):
      authentication = UNSET
    else:
      authentication = AuthenticationType(_authentication)

    def _parse_sqlite_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sqlite_version = _parse_sqlite_version(d.pop("sqliteVersion", UNSET))

    migration_version = d.pop("migrationVersion", UNSET)

    def _parse_url_base(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    url_base = _parse_url_base(d.pop("urlBase", UNSET))

    def _parse_runtime_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    runtime_version = _parse_runtime_version(d.pop("runtimeVersion", UNSET))

    def _parse_runtime_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    runtime_name = _parse_runtime_name(d.pop("runtimeName", UNSET))

    _start_time = d.pop("startTime", UNSET)
    start_time: datetime.datetime | Unset
    if isinstance(_start_time, Unset):
      start_time = UNSET
    else:
      start_time = isoparse(_start_time)

    def _parse_package_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    package_version = _parse_package_version(d.pop("packageVersion", UNSET))

    def _parse_package_author(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    package_author = _parse_package_author(d.pop("packageAuthor", UNSET))

    _package_update_mechanism = d.pop("packageUpdateMechanism", UNSET)
    package_update_mechanism: UpdateMechanism | Unset
    if isinstance(_package_update_mechanism, Unset):
      package_update_mechanism = UNSET
    else:
      package_update_mechanism = UpdateMechanism(_package_update_mechanism)

    def _parse_package_update_mechanism_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    package_update_mechanism_message = _parse_package_update_mechanism_message(
      d.pop("packageUpdateMechanismMessage", UNSET)
    )

    def _parse_database_version(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    database_version = _parse_database_version(d.pop("databaseVersion", UNSET))

    _database_type = d.pop("databaseType", UNSET)
    database_type: DatabaseType | Unset
    if isinstance(_database_type, Unset):
      database_type = UNSET
    else:
      database_type = DatabaseType(_database_type)

    system_resource = cls(
      app_name=app_name,
      instance_name=instance_name,
      version=version,
      build_time=build_time,
      is_debug=is_debug,
      is_production=is_production,
      is_admin=is_admin,
      is_user_interactive=is_user_interactive,
      startup_path=startup_path,
      app_data=app_data,
      os_name=os_name,
      os_version=os_version,
      is_net_core=is_net_core,
      is_linux=is_linux,
      is_osx=is_osx,
      is_windows=is_windows,
      is_docker=is_docker,
      mode=mode,
      branch=branch,
      authentication=authentication,
      sqlite_version=sqlite_version,
      migration_version=migration_version,
      url_base=url_base,
      runtime_version=runtime_version,
      runtime_name=runtime_name,
      start_time=start_time,
      package_version=package_version,
      package_author=package_author,
      package_update_mechanism=package_update_mechanism,
      package_update_mechanism_message=package_update_mechanism_message,
      database_version=database_version,
      database_type=database_type,
    )

    return system_resource
