from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.unmapped_folder import UnmappedFolder


T = TypeVar("T", bound="RootFolderResource")


@_attrs_define
class RootFolderResource:
  """
  Attributes:
      id (int | Unset):
      path (None | str | Unset):
      accessible (bool | Unset):
      free_space (int | None | Unset):
      unmapped_folders (list[UnmappedFolder] | None | Unset):
  """

  id: int | Unset = UNSET
  path: None | str | Unset = UNSET
  accessible: bool | Unset = UNSET
  free_space: int | None | Unset = UNSET
  unmapped_folders: list[UnmappedFolder] | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    accessible = self.accessible

    free_space: int | None | Unset
    if isinstance(self.free_space, Unset):
      free_space = UNSET
    else:
      free_space = self.free_space

    unmapped_folders: list[dict[str, Any]] | None | Unset
    if isinstance(self.unmapped_folders, Unset):
      unmapped_folders = UNSET
    elif isinstance(self.unmapped_folders, list):
      unmapped_folders = []
      for unmapped_folders_type_0_item_data in self.unmapped_folders:
        unmapped_folders_type_0_item = unmapped_folders_type_0_item_data.to_dict()
        unmapped_folders.append(unmapped_folders_type_0_item)

    else:
      unmapped_folders = self.unmapped_folders

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if path is not UNSET:
      field_dict["path"] = path
    if accessible is not UNSET:
      field_dict["accessible"] = accessible
    if free_space is not UNSET:
      field_dict["freeSpace"] = free_space
    if unmapped_folders is not UNSET:
      field_dict["unmappedFolders"] = unmapped_folders

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.unmapped_folder import UnmappedFolder

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    accessible = d.pop("accessible", UNSET)

    def _parse_free_space(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    free_space = _parse_free_space(d.pop("freeSpace", UNSET))

    def _parse_unmapped_folders(data: object) -> list[UnmappedFolder] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        unmapped_folders_type_0 = []
        _unmapped_folders_type_0 = data
        for unmapped_folders_type_0_item_data in _unmapped_folders_type_0:
          unmapped_folders_type_0_item = UnmappedFolder.from_dict(unmapped_folders_type_0_item_data)

          unmapped_folders_type_0.append(unmapped_folders_type_0_item)

        return unmapped_folders_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[UnmappedFolder] | None | Unset, data)

    unmapped_folders = _parse_unmapped_folders(d.pop("unmappedFolders", UNSET))

    root_folder_resource = cls(
      id=id,
      path=path,
      accessible=accessible,
      free_space=free_space,
      unmapped_folders=unmapped_folders,
    )

    return root_folder_resource
