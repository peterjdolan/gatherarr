from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.authentication_required_type import AuthenticationRequiredType
from ..models.authentication_type import AuthenticationType
from ..models.certificate_validation_type import CertificateValidationType
from ..models.proxy_type import ProxyType
from ..models.update_mechanism import UpdateMechanism
from ..types import UNSET, Unset

T = TypeVar("T", bound="HostConfigResource")


@_attrs_define
class HostConfigResource:
  """
  Attributes:
      id (int | Unset):
      bind_address (None | str | Unset):
      port (int | Unset):
      ssl_port (int | Unset):
      enable_ssl (bool | Unset):
      launch_browser (bool | Unset):
      authentication_method (AuthenticationType | Unset):
      authentication_required (AuthenticationRequiredType | Unset):
      analytics_enabled (bool | Unset):
      username (None | str | Unset):
      password (None | str | Unset):
      password_confirmation (None | str | Unset):
      log_level (None | str | Unset):
      log_size_limit (int | Unset):
      console_log_level (None | str | Unset):
      branch (None | str | Unset):
      api_key (None | str | Unset):
      ssl_cert_path (None | str | Unset):
      ssl_cert_password (None | str | Unset):
      url_base (None | str | Unset):
      instance_name (None | str | Unset):
      application_url (None | str | Unset):
      update_automatically (bool | Unset):
      update_mechanism (UpdateMechanism | Unset):
      update_script_path (None | str | Unset):
      proxy_enabled (bool | Unset):
      proxy_type (ProxyType | Unset):
      proxy_hostname (None | str | Unset):
      proxy_port (int | Unset):
      proxy_username (None | str | Unset):
      proxy_password (None | str | Unset):
      proxy_bypass_filter (None | str | Unset):
      proxy_bypass_local_addresses (bool | Unset):
      certificate_validation (CertificateValidationType | Unset):
      backup_folder (None | str | Unset):
      backup_interval (int | Unset):
      backup_retention (int | Unset):
      trust_cgnat_ip_addresses (bool | Unset):
  """

  id: int | Unset = UNSET
  bind_address: None | str | Unset = UNSET
  port: int | Unset = UNSET
  ssl_port: int | Unset = UNSET
  enable_ssl: bool | Unset = UNSET
  launch_browser: bool | Unset = UNSET
  authentication_method: AuthenticationType | Unset = UNSET
  authentication_required: AuthenticationRequiredType | Unset = UNSET
  analytics_enabled: bool | Unset = UNSET
  username: None | str | Unset = UNSET
  password: None | str | Unset = UNSET
  password_confirmation: None | str | Unset = UNSET
  log_level: None | str | Unset = UNSET
  log_size_limit: int | Unset = UNSET
  console_log_level: None | str | Unset = UNSET
  branch: None | str | Unset = UNSET
  api_key: None | str | Unset = UNSET
  ssl_cert_path: None | str | Unset = UNSET
  ssl_cert_password: None | str | Unset = UNSET
  url_base: None | str | Unset = UNSET
  instance_name: None | str | Unset = UNSET
  application_url: None | str | Unset = UNSET
  update_automatically: bool | Unset = UNSET
  update_mechanism: UpdateMechanism | Unset = UNSET
  update_script_path: None | str | Unset = UNSET
  proxy_enabled: bool | Unset = UNSET
  proxy_type: ProxyType | Unset = UNSET
  proxy_hostname: None | str | Unset = UNSET
  proxy_port: int | Unset = UNSET
  proxy_username: None | str | Unset = UNSET
  proxy_password: None | str | Unset = UNSET
  proxy_bypass_filter: None | str | Unset = UNSET
  proxy_bypass_local_addresses: bool | Unset = UNSET
  certificate_validation: CertificateValidationType | Unset = UNSET
  backup_folder: None | str | Unset = UNSET
  backup_interval: int | Unset = UNSET
  backup_retention: int | Unset = UNSET
  trust_cgnat_ip_addresses: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    bind_address: None | str | Unset
    if isinstance(self.bind_address, Unset):
      bind_address = UNSET
    else:
      bind_address = self.bind_address

    port = self.port

    ssl_port = self.ssl_port

    enable_ssl = self.enable_ssl

    launch_browser = self.launch_browser

    authentication_method: str | Unset = UNSET
    if not isinstance(self.authentication_method, Unset):
      authentication_method = self.authentication_method.value

    authentication_required: str | Unset = UNSET
    if not isinstance(self.authentication_required, Unset):
      authentication_required = self.authentication_required.value

    analytics_enabled = self.analytics_enabled

    username: None | str | Unset
    if isinstance(self.username, Unset):
      username = UNSET
    else:
      username = self.username

    password: None | str | Unset
    if isinstance(self.password, Unset):
      password = UNSET
    else:
      password = self.password

    password_confirmation: None | str | Unset
    if isinstance(self.password_confirmation, Unset):
      password_confirmation = UNSET
    else:
      password_confirmation = self.password_confirmation

    log_level: None | str | Unset
    if isinstance(self.log_level, Unset):
      log_level = UNSET
    else:
      log_level = self.log_level

    log_size_limit = self.log_size_limit

    console_log_level: None | str | Unset
    if isinstance(self.console_log_level, Unset):
      console_log_level = UNSET
    else:
      console_log_level = self.console_log_level

    branch: None | str | Unset
    if isinstance(self.branch, Unset):
      branch = UNSET
    else:
      branch = self.branch

    api_key: None | str | Unset
    if isinstance(self.api_key, Unset):
      api_key = UNSET
    else:
      api_key = self.api_key

    ssl_cert_path: None | str | Unset
    if isinstance(self.ssl_cert_path, Unset):
      ssl_cert_path = UNSET
    else:
      ssl_cert_path = self.ssl_cert_path

    ssl_cert_password: None | str | Unset
    if isinstance(self.ssl_cert_password, Unset):
      ssl_cert_password = UNSET
    else:
      ssl_cert_password = self.ssl_cert_password

    url_base: None | str | Unset
    if isinstance(self.url_base, Unset):
      url_base = UNSET
    else:
      url_base = self.url_base

    instance_name: None | str | Unset
    if isinstance(self.instance_name, Unset):
      instance_name = UNSET
    else:
      instance_name = self.instance_name

    application_url: None | str | Unset
    if isinstance(self.application_url, Unset):
      application_url = UNSET
    else:
      application_url = self.application_url

    update_automatically = self.update_automatically

    update_mechanism: str | Unset = UNSET
    if not isinstance(self.update_mechanism, Unset):
      update_mechanism = self.update_mechanism.value

    update_script_path: None | str | Unset
    if isinstance(self.update_script_path, Unset):
      update_script_path = UNSET
    else:
      update_script_path = self.update_script_path

    proxy_enabled = self.proxy_enabled

    proxy_type: str | Unset = UNSET
    if not isinstance(self.proxy_type, Unset):
      proxy_type = self.proxy_type.value

    proxy_hostname: None | str | Unset
    if isinstance(self.proxy_hostname, Unset):
      proxy_hostname = UNSET
    else:
      proxy_hostname = self.proxy_hostname

    proxy_port = self.proxy_port

    proxy_username: None | str | Unset
    if isinstance(self.proxy_username, Unset):
      proxy_username = UNSET
    else:
      proxy_username = self.proxy_username

    proxy_password: None | str | Unset
    if isinstance(self.proxy_password, Unset):
      proxy_password = UNSET
    else:
      proxy_password = self.proxy_password

    proxy_bypass_filter: None | str | Unset
    if isinstance(self.proxy_bypass_filter, Unset):
      proxy_bypass_filter = UNSET
    else:
      proxy_bypass_filter = self.proxy_bypass_filter

    proxy_bypass_local_addresses = self.proxy_bypass_local_addresses

    certificate_validation: str | Unset = UNSET
    if not isinstance(self.certificate_validation, Unset):
      certificate_validation = self.certificate_validation.value

    backup_folder: None | str | Unset
    if isinstance(self.backup_folder, Unset):
      backup_folder = UNSET
    else:
      backup_folder = self.backup_folder

    backup_interval = self.backup_interval

    backup_retention = self.backup_retention

    trust_cgnat_ip_addresses = self.trust_cgnat_ip_addresses

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if bind_address is not UNSET:
      field_dict["bindAddress"] = bind_address
    if port is not UNSET:
      field_dict["port"] = port
    if ssl_port is not UNSET:
      field_dict["sslPort"] = ssl_port
    if enable_ssl is not UNSET:
      field_dict["enableSsl"] = enable_ssl
    if launch_browser is not UNSET:
      field_dict["launchBrowser"] = launch_browser
    if authentication_method is not UNSET:
      field_dict["authenticationMethod"] = authentication_method
    if authentication_required is not UNSET:
      field_dict["authenticationRequired"] = authentication_required
    if analytics_enabled is not UNSET:
      field_dict["analyticsEnabled"] = analytics_enabled
    if username is not UNSET:
      field_dict["username"] = username
    if password is not UNSET:
      field_dict["password"] = password
    if password_confirmation is not UNSET:
      field_dict["passwordConfirmation"] = password_confirmation
    if log_level is not UNSET:
      field_dict["logLevel"] = log_level
    if log_size_limit is not UNSET:
      field_dict["logSizeLimit"] = log_size_limit
    if console_log_level is not UNSET:
      field_dict["consoleLogLevel"] = console_log_level
    if branch is not UNSET:
      field_dict["branch"] = branch
    if api_key is not UNSET:
      field_dict["apiKey"] = api_key
    if ssl_cert_path is not UNSET:
      field_dict["sslCertPath"] = ssl_cert_path
    if ssl_cert_password is not UNSET:
      field_dict["sslCertPassword"] = ssl_cert_password
    if url_base is not UNSET:
      field_dict["urlBase"] = url_base
    if instance_name is not UNSET:
      field_dict["instanceName"] = instance_name
    if application_url is not UNSET:
      field_dict["applicationUrl"] = application_url
    if update_automatically is not UNSET:
      field_dict["updateAutomatically"] = update_automatically
    if update_mechanism is not UNSET:
      field_dict["updateMechanism"] = update_mechanism
    if update_script_path is not UNSET:
      field_dict["updateScriptPath"] = update_script_path
    if proxy_enabled is not UNSET:
      field_dict["proxyEnabled"] = proxy_enabled
    if proxy_type is not UNSET:
      field_dict["proxyType"] = proxy_type
    if proxy_hostname is not UNSET:
      field_dict["proxyHostname"] = proxy_hostname
    if proxy_port is not UNSET:
      field_dict["proxyPort"] = proxy_port
    if proxy_username is not UNSET:
      field_dict["proxyUsername"] = proxy_username
    if proxy_password is not UNSET:
      field_dict["proxyPassword"] = proxy_password
    if proxy_bypass_filter is not UNSET:
      field_dict["proxyBypassFilter"] = proxy_bypass_filter
    if proxy_bypass_local_addresses is not UNSET:
      field_dict["proxyBypassLocalAddresses"] = proxy_bypass_local_addresses
    if certificate_validation is not UNSET:
      field_dict["certificateValidation"] = certificate_validation
    if backup_folder is not UNSET:
      field_dict["backupFolder"] = backup_folder
    if backup_interval is not UNSET:
      field_dict["backupInterval"] = backup_interval
    if backup_retention is not UNSET:
      field_dict["backupRetention"] = backup_retention
    if trust_cgnat_ip_addresses is not UNSET:
      field_dict["trustCgnatIpAddresses"] = trust_cgnat_ip_addresses

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_bind_address(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    bind_address = _parse_bind_address(d.pop("bindAddress", UNSET))

    port = d.pop("port", UNSET)

    ssl_port = d.pop("sslPort", UNSET)

    enable_ssl = d.pop("enableSsl", UNSET)

    launch_browser = d.pop("launchBrowser", UNSET)

    _authentication_method = d.pop("authenticationMethod", UNSET)
    authentication_method: AuthenticationType | Unset
    if isinstance(_authentication_method, Unset):
      authentication_method = UNSET
    else:
      authentication_method = AuthenticationType(_authentication_method)

    _authentication_required = d.pop("authenticationRequired", UNSET)
    authentication_required: AuthenticationRequiredType | Unset
    if isinstance(_authentication_required, Unset):
      authentication_required = UNSET
    else:
      authentication_required = AuthenticationRequiredType(_authentication_required)

    analytics_enabled = d.pop("analyticsEnabled", UNSET)

    def _parse_username(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    username = _parse_username(d.pop("username", UNSET))

    def _parse_password(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    password = _parse_password(d.pop("password", UNSET))

    def _parse_password_confirmation(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    password_confirmation = _parse_password_confirmation(d.pop("passwordConfirmation", UNSET))

    def _parse_log_level(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    log_level = _parse_log_level(d.pop("logLevel", UNSET))

    log_size_limit = d.pop("logSizeLimit", UNSET)

    def _parse_console_log_level(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    console_log_level = _parse_console_log_level(d.pop("consoleLogLevel", UNSET))

    def _parse_branch(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    branch = _parse_branch(d.pop("branch", UNSET))

    def _parse_api_key(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    api_key = _parse_api_key(d.pop("apiKey", UNSET))

    def _parse_ssl_cert_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    ssl_cert_path = _parse_ssl_cert_path(d.pop("sslCertPath", UNSET))

    def _parse_ssl_cert_password(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    ssl_cert_password = _parse_ssl_cert_password(d.pop("sslCertPassword", UNSET))

    def _parse_url_base(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    url_base = _parse_url_base(d.pop("urlBase", UNSET))

    def _parse_instance_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    instance_name = _parse_instance_name(d.pop("instanceName", UNSET))

    def _parse_application_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    application_url = _parse_application_url(d.pop("applicationUrl", UNSET))

    update_automatically = d.pop("updateAutomatically", UNSET)

    _update_mechanism = d.pop("updateMechanism", UNSET)
    update_mechanism: UpdateMechanism | Unset
    if isinstance(_update_mechanism, Unset):
      update_mechanism = UNSET
    else:
      update_mechanism = UpdateMechanism(_update_mechanism)

    def _parse_update_script_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    update_script_path = _parse_update_script_path(d.pop("updateScriptPath", UNSET))

    proxy_enabled = d.pop("proxyEnabled", UNSET)

    _proxy_type = d.pop("proxyType", UNSET)
    proxy_type: ProxyType | Unset
    if isinstance(_proxy_type, Unset):
      proxy_type = UNSET
    else:
      proxy_type = ProxyType(_proxy_type)

    def _parse_proxy_hostname(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    proxy_hostname = _parse_proxy_hostname(d.pop("proxyHostname", UNSET))

    proxy_port = d.pop("proxyPort", UNSET)

    def _parse_proxy_username(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    proxy_username = _parse_proxy_username(d.pop("proxyUsername", UNSET))

    def _parse_proxy_password(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    proxy_password = _parse_proxy_password(d.pop("proxyPassword", UNSET))

    def _parse_proxy_bypass_filter(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    proxy_bypass_filter = _parse_proxy_bypass_filter(d.pop("proxyBypassFilter", UNSET))

    proxy_bypass_local_addresses = d.pop("proxyBypassLocalAddresses", UNSET)

    _certificate_validation = d.pop("certificateValidation", UNSET)
    certificate_validation: CertificateValidationType | Unset
    if isinstance(_certificate_validation, Unset):
      certificate_validation = UNSET
    else:
      certificate_validation = CertificateValidationType(_certificate_validation)

    def _parse_backup_folder(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    backup_folder = _parse_backup_folder(d.pop("backupFolder", UNSET))

    backup_interval = d.pop("backupInterval", UNSET)

    backup_retention = d.pop("backupRetention", UNSET)

    trust_cgnat_ip_addresses = d.pop("trustCgnatIpAddresses", UNSET)

    host_config_resource = cls(
      id=id,
      bind_address=bind_address,
      port=port,
      ssl_port=ssl_port,
      enable_ssl=enable_ssl,
      launch_browser=launch_browser,
      authentication_method=authentication_method,
      authentication_required=authentication_required,
      analytics_enabled=analytics_enabled,
      username=username,
      password=password,
      password_confirmation=password_confirmation,
      log_level=log_level,
      log_size_limit=log_size_limit,
      console_log_level=console_log_level,
      branch=branch,
      api_key=api_key,
      ssl_cert_path=ssl_cert_path,
      ssl_cert_password=ssl_cert_password,
      url_base=url_base,
      instance_name=instance_name,
      application_url=application_url,
      update_automatically=update_automatically,
      update_mechanism=update_mechanism,
      update_script_path=update_script_path,
      proxy_enabled=proxy_enabled,
      proxy_type=proxy_type,
      proxy_hostname=proxy_hostname,
      proxy_port=proxy_port,
      proxy_username=proxy_username,
      proxy_password=proxy_password,
      proxy_bypass_filter=proxy_bypass_filter,
      proxy_bypass_local_addresses=proxy_bypass_local_addresses,
      certificate_validation=certificate_validation,
      backup_folder=backup_folder,
      backup_interval=backup_interval,
      backup_retention=backup_retention,
      trust_cgnat_ip_addresses=trust_cgnat_ip_addresses,
    )

    return host_config_resource
