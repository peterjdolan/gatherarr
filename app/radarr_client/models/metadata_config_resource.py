from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.tm_db_country_code import TMDbCountryCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataConfigResource")


@_attrs_define
class MetadataConfigResource:
  """
  Attributes:
      id (int | Unset):
      certification_country (TMDbCountryCode | Unset):
  """

  id: int | Unset = UNSET
  certification_country: TMDbCountryCode | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    certification_country: str | Unset = UNSET
    if not isinstance(self.certification_country, Unset):
      certification_country = self.certification_country.value

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if certification_country is not UNSET:
      field_dict["certificationCountry"] = certification_country

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    _certification_country = d.pop("certificationCountry", UNSET)
    certification_country: TMDbCountryCode | Unset
    if isinstance(_certification_country, Unset):
      certification_country = UNSET
    else:
      certification_country = TMDbCountryCode(_certification_country)

    metadata_config_resource = cls(
      id=id,
      certification_country=certification_country,
    )

    return metadata_config_resource
