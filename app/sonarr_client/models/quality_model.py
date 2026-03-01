from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.quality import Quality
  from ..models.revision import Revision


T = TypeVar("T", bound="QualityModel")


@_attrs_define
class QualityModel:
  """
  Attributes:
      quality (Quality | Unset):
      revision (Revision | Unset):
  """

  quality: Quality | Unset = UNSET
  revision: Revision | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    revision: dict[str, Any] | Unset = UNSET
    if not isinstance(self.revision, Unset):
      revision = self.revision.to_dict()

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if quality is not UNSET:
      field_dict["quality"] = quality
    if revision is not UNSET:
      field_dict["revision"] = revision

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.quality import Quality
    from ..models.revision import Revision

    d = dict(src_dict)
    _quality = d.pop("quality", UNSET)
    quality: Quality | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = Quality.from_dict(_quality)

    _revision = d.pop("revision", UNSET)
    revision: Revision | Unset
    if isinstance(_revision, Unset):
      revision = UNSET
    else:
      revision = Revision.from_dict(_revision)

    quality_model = cls(
      quality=quality,
      revision=revision,
    )

    return quality_model
