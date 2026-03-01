from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.file_date_type import FileDateType
from ..models.proper_download_types import ProperDownloadTypes
from ..models.rescan_after_refresh_type import RescanAfterRefreshType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaManagementConfigResource")


@_attrs_define
class MediaManagementConfigResource:
  """
  Attributes:
      id (int | Unset):
      auto_unmonitor_previously_downloaded_movies (bool | Unset):
      recycle_bin (None | str | Unset):
      recycle_bin_cleanup_days (int | Unset):
      download_propers_and_repacks (ProperDownloadTypes | Unset):
      create_empty_movie_folders (bool | Unset):
      delete_empty_folders (bool | Unset):
      file_date (FileDateType | Unset):
      rescan_after_refresh (RescanAfterRefreshType | Unset):
      auto_rename_folders (bool | Unset):
      paths_default_static (bool | Unset):
      set_permissions_linux (bool | Unset):
      chmod_folder (None | str | Unset):
      chown_group (None | str | Unset):
      skip_free_space_check_when_importing (bool | Unset):
      minimum_free_space_when_importing (int | Unset):
      copy_using_hardlinks (bool | Unset):
      use_script_import (bool | Unset):
      script_import_path (None | str | Unset):
      import_extra_files (bool | Unset):
      extra_file_extensions (None | str | Unset):
      enable_media_info (bool | Unset):
  """

  id: int | Unset = UNSET
  auto_unmonitor_previously_downloaded_movies: bool | Unset = UNSET
  recycle_bin: None | str | Unset = UNSET
  recycle_bin_cleanup_days: int | Unset = UNSET
  download_propers_and_repacks: ProperDownloadTypes | Unset = UNSET
  create_empty_movie_folders: bool | Unset = UNSET
  delete_empty_folders: bool | Unset = UNSET
  file_date: FileDateType | Unset = UNSET
  rescan_after_refresh: RescanAfterRefreshType | Unset = UNSET
  auto_rename_folders: bool | Unset = UNSET
  paths_default_static: bool | Unset = UNSET
  set_permissions_linux: bool | Unset = UNSET
  chmod_folder: None | str | Unset = UNSET
  chown_group: None | str | Unset = UNSET
  skip_free_space_check_when_importing: bool | Unset = UNSET
  minimum_free_space_when_importing: int | Unset = UNSET
  copy_using_hardlinks: bool | Unset = UNSET
  use_script_import: bool | Unset = UNSET
  script_import_path: None | str | Unset = UNSET
  import_extra_files: bool | Unset = UNSET
  extra_file_extensions: None | str | Unset = UNSET
  enable_media_info: bool | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    auto_unmonitor_previously_downloaded_movies = self.auto_unmonitor_previously_downloaded_movies

    recycle_bin: None | str | Unset
    if isinstance(self.recycle_bin, Unset):
      recycle_bin = UNSET
    else:
      recycle_bin = self.recycle_bin

    recycle_bin_cleanup_days = self.recycle_bin_cleanup_days

    download_propers_and_repacks: str | Unset = UNSET
    if not isinstance(self.download_propers_and_repacks, Unset):
      download_propers_and_repacks = self.download_propers_and_repacks.value

    create_empty_movie_folders = self.create_empty_movie_folders

    delete_empty_folders = self.delete_empty_folders

    file_date: str | Unset = UNSET
    if not isinstance(self.file_date, Unset):
      file_date = self.file_date.value

    rescan_after_refresh: str | Unset = UNSET
    if not isinstance(self.rescan_after_refresh, Unset):
      rescan_after_refresh = self.rescan_after_refresh.value

    auto_rename_folders = self.auto_rename_folders

    paths_default_static = self.paths_default_static

    set_permissions_linux = self.set_permissions_linux

    chmod_folder: None | str | Unset
    if isinstance(self.chmod_folder, Unset):
      chmod_folder = UNSET
    else:
      chmod_folder = self.chmod_folder

    chown_group: None | str | Unset
    if isinstance(self.chown_group, Unset):
      chown_group = UNSET
    else:
      chown_group = self.chown_group

    skip_free_space_check_when_importing = self.skip_free_space_check_when_importing

    minimum_free_space_when_importing = self.minimum_free_space_when_importing

    copy_using_hardlinks = self.copy_using_hardlinks

    use_script_import = self.use_script_import

    script_import_path: None | str | Unset
    if isinstance(self.script_import_path, Unset):
      script_import_path = UNSET
    else:
      script_import_path = self.script_import_path

    import_extra_files = self.import_extra_files

    extra_file_extensions: None | str | Unset
    if isinstance(self.extra_file_extensions, Unset):
      extra_file_extensions = UNSET
    else:
      extra_file_extensions = self.extra_file_extensions

    enable_media_info = self.enable_media_info

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if auto_unmonitor_previously_downloaded_movies is not UNSET:
      field_dict["autoUnmonitorPreviouslyDownloadedMovies"] = (
        auto_unmonitor_previously_downloaded_movies
      )
    if recycle_bin is not UNSET:
      field_dict["recycleBin"] = recycle_bin
    if recycle_bin_cleanup_days is not UNSET:
      field_dict["recycleBinCleanupDays"] = recycle_bin_cleanup_days
    if download_propers_and_repacks is not UNSET:
      field_dict["downloadPropersAndRepacks"] = download_propers_and_repacks
    if create_empty_movie_folders is not UNSET:
      field_dict["createEmptyMovieFolders"] = create_empty_movie_folders
    if delete_empty_folders is not UNSET:
      field_dict["deleteEmptyFolders"] = delete_empty_folders
    if file_date is not UNSET:
      field_dict["fileDate"] = file_date
    if rescan_after_refresh is not UNSET:
      field_dict["rescanAfterRefresh"] = rescan_after_refresh
    if auto_rename_folders is not UNSET:
      field_dict["autoRenameFolders"] = auto_rename_folders
    if paths_default_static is not UNSET:
      field_dict["pathsDefaultStatic"] = paths_default_static
    if set_permissions_linux is not UNSET:
      field_dict["setPermissionsLinux"] = set_permissions_linux
    if chmod_folder is not UNSET:
      field_dict["chmodFolder"] = chmod_folder
    if chown_group is not UNSET:
      field_dict["chownGroup"] = chown_group
    if skip_free_space_check_when_importing is not UNSET:
      field_dict["skipFreeSpaceCheckWhenImporting"] = skip_free_space_check_when_importing
    if minimum_free_space_when_importing is not UNSET:
      field_dict["minimumFreeSpaceWhenImporting"] = minimum_free_space_when_importing
    if copy_using_hardlinks is not UNSET:
      field_dict["copyUsingHardlinks"] = copy_using_hardlinks
    if use_script_import is not UNSET:
      field_dict["useScriptImport"] = use_script_import
    if script_import_path is not UNSET:
      field_dict["scriptImportPath"] = script_import_path
    if import_extra_files is not UNSET:
      field_dict["importExtraFiles"] = import_extra_files
    if extra_file_extensions is not UNSET:
      field_dict["extraFileExtensions"] = extra_file_extensions
    if enable_media_info is not UNSET:
      field_dict["enableMediaInfo"] = enable_media_info

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    auto_unmonitor_previously_downloaded_movies = d.pop(
      "autoUnmonitorPreviouslyDownloadedMovies", UNSET
    )

    def _parse_recycle_bin(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    recycle_bin = _parse_recycle_bin(d.pop("recycleBin", UNSET))

    recycle_bin_cleanup_days = d.pop("recycleBinCleanupDays", UNSET)

    _download_propers_and_repacks = d.pop("downloadPropersAndRepacks", UNSET)
    download_propers_and_repacks: ProperDownloadTypes | Unset
    if isinstance(_download_propers_and_repacks, Unset):
      download_propers_and_repacks = UNSET
    else:
      download_propers_and_repacks = ProperDownloadTypes(_download_propers_and_repacks)

    create_empty_movie_folders = d.pop("createEmptyMovieFolders", UNSET)

    delete_empty_folders = d.pop("deleteEmptyFolders", UNSET)

    _file_date = d.pop("fileDate", UNSET)
    file_date: FileDateType | Unset
    if isinstance(_file_date, Unset):
      file_date = UNSET
    else:
      file_date = FileDateType(_file_date)

    _rescan_after_refresh = d.pop("rescanAfterRefresh", UNSET)
    rescan_after_refresh: RescanAfterRefreshType | Unset
    if isinstance(_rescan_after_refresh, Unset):
      rescan_after_refresh = UNSET
    else:
      rescan_after_refresh = RescanAfterRefreshType(_rescan_after_refresh)

    auto_rename_folders = d.pop("autoRenameFolders", UNSET)

    paths_default_static = d.pop("pathsDefaultStatic", UNSET)

    set_permissions_linux = d.pop("setPermissionsLinux", UNSET)

    def _parse_chmod_folder(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    chmod_folder = _parse_chmod_folder(d.pop("chmodFolder", UNSET))

    def _parse_chown_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    chown_group = _parse_chown_group(d.pop("chownGroup", UNSET))

    skip_free_space_check_when_importing = d.pop("skipFreeSpaceCheckWhenImporting", UNSET)

    minimum_free_space_when_importing = d.pop("minimumFreeSpaceWhenImporting", UNSET)

    copy_using_hardlinks = d.pop("copyUsingHardlinks", UNSET)

    use_script_import = d.pop("useScriptImport", UNSET)

    def _parse_script_import_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    script_import_path = _parse_script_import_path(d.pop("scriptImportPath", UNSET))

    import_extra_files = d.pop("importExtraFiles", UNSET)

    def _parse_extra_file_extensions(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    extra_file_extensions = _parse_extra_file_extensions(d.pop("extraFileExtensions", UNSET))

    enable_media_info = d.pop("enableMediaInfo", UNSET)

    media_management_config_resource = cls(
      id=id,
      auto_unmonitor_previously_downloaded_movies=auto_unmonitor_previously_downloaded_movies,
      recycle_bin=recycle_bin,
      recycle_bin_cleanup_days=recycle_bin_cleanup_days,
      download_propers_and_repacks=download_propers_and_repacks,
      create_empty_movie_folders=create_empty_movie_folders,
      delete_empty_folders=delete_empty_folders,
      file_date=file_date,
      rescan_after_refresh=rescan_after_refresh,
      auto_rename_folders=auto_rename_folders,
      paths_default_static=paths_default_static,
      set_permissions_linux=set_permissions_linux,
      chmod_folder=chmod_folder,
      chown_group=chown_group,
      skip_free_space_check_when_importing=skip_free_space_check_when_importing,
      minimum_free_space_when_importing=minimum_free_space_when_importing,
      copy_using_hardlinks=copy_using_hardlinks,
      use_script_import=use_script_import,
      script_import_path=script_import_path,
      import_extra_files=import_extra_files,
      extra_file_extensions=extra_file_extensions,
      enable_media_info=enable_media_info,
    )

    return media_management_config_resource
