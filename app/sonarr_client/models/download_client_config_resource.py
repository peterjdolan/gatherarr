from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DownloadClientConfigResource")


@_attrs_define
class DownloadClientConfigResource:
  """
  Attributes:
      id (int | Unset):
      download_client_working_folders (None | str | Unset):
      enable_completed_download_handling (bool | Unset):
      auto_redownload_failed (bool | Unset):
      auto_redownload_failed_from_interactive_search (bool | Unset):
  """

  id: int | Unset = UNSET
  download_client_working_folders: None | str | Unset = UNSET
  enable_completed_download_handling: bool | Unset = UNSET
  auto_redownload_failed: bool | Unset = UNSET
  auto_redownload_failed_from_interactive_search: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    download_client_working_folders: None | str | Unset
    if isinstance(self.download_client_working_folders, Unset):
      download_client_working_folders = UNSET
    else:
      download_client_working_folders = self.download_client_working_folders

    enable_completed_download_handling = self.enable_completed_download_handling

    auto_redownload_failed = self.auto_redownload_failed

    auto_redownload_failed_from_interactive_search = (
      self.auto_redownload_failed_from_interactive_search
    )

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if download_client_working_folders is not UNSET:
      field_dict["downloadClientWorkingFolders"] = download_client_working_folders
    if enable_completed_download_handling is not UNSET:
      field_dict["enableCompletedDownloadHandling"] = enable_completed_download_handling
    if auto_redownload_failed is not UNSET:
      field_dict["autoRedownloadFailed"] = auto_redownload_failed
    if auto_redownload_failed_from_interactive_search is not UNSET:
      field_dict["autoRedownloadFailedFromInteractiveSearch"] = (
        auto_redownload_failed_from_interactive_search
      )

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_download_client_working_folders(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_client_working_folders = _parse_download_client_working_folders(
      d.pop("downloadClientWorkingFolders", UNSET)
    )

    enable_completed_download_handling = d.pop("enableCompletedDownloadHandling", UNSET)

    auto_redownload_failed = d.pop("autoRedownloadFailed", UNSET)

    auto_redownload_failed_from_interactive_search = d.pop(
      "autoRedownloadFailedFromInteractiveSearch", UNSET
    )

    download_client_config_resource = cls(
      id=id,
      download_client_working_folders=download_client_working_folders,
      enable_completed_download_handling=enable_completed_download_handling,
      auto_redownload_failed=auto_redownload_failed,
      auto_redownload_failed_from_interactive_search=auto_redownload_failed_from_interactive_search,
    )

    return download_client_config_resource
