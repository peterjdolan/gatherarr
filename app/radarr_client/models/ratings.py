from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.rating_child import RatingChild


T = TypeVar("T", bound="Ratings")


@_attrs_define
class Ratings:
  """
  Attributes:
      imdb (RatingChild | Unset):
      tmdb (RatingChild | Unset):
      metacritic (RatingChild | Unset):
      rotten_tomatoes (RatingChild | Unset):
      trakt (RatingChild | Unset):
  """

  imdb: RatingChild | Unset = UNSET
  tmdb: RatingChild | Unset = UNSET
  metacritic: RatingChild | Unset = UNSET
  rotten_tomatoes: RatingChild | Unset = UNSET
  trakt: RatingChild | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    imdb: dict[str, Any] | Unset = UNSET
    if not isinstance(self.imdb, Unset):
      imdb = self.imdb.to_dict()

    tmdb: dict[str, Any] | Unset = UNSET
    if not isinstance(self.tmdb, Unset):
      tmdb = self.tmdb.to_dict()

    metacritic: dict[str, Any] | Unset = UNSET
    if not isinstance(self.metacritic, Unset):
      metacritic = self.metacritic.to_dict()

    rotten_tomatoes: dict[str, Any] | Unset = UNSET
    if not isinstance(self.rotten_tomatoes, Unset):
      rotten_tomatoes = self.rotten_tomatoes.to_dict()

    trakt: dict[str, Any] | Unset = UNSET
    if not isinstance(self.trakt, Unset):
      trakt = self.trakt.to_dict()

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if imdb is not UNSET:
      field_dict["imdb"] = imdb
    if tmdb is not UNSET:
      field_dict["tmdb"] = tmdb
    if metacritic is not UNSET:
      field_dict["metacritic"] = metacritic
    if rotten_tomatoes is not UNSET:
      field_dict["rottenTomatoes"] = rotten_tomatoes
    if trakt is not UNSET:
      field_dict["trakt"] = trakt

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.rating_child import RatingChild

    d = dict(src_dict)
    _imdb = d.pop("imdb", UNSET)
    imdb: RatingChild | Unset
    if isinstance(_imdb, Unset):
      imdb = UNSET
    else:
      imdb = RatingChild.from_dict(_imdb)

    _tmdb = d.pop("tmdb", UNSET)
    tmdb: RatingChild | Unset
    if isinstance(_tmdb, Unset):
      tmdb = UNSET
    else:
      tmdb = RatingChild.from_dict(_tmdb)

    _metacritic = d.pop("metacritic", UNSET)
    metacritic: RatingChild | Unset
    if isinstance(_metacritic, Unset):
      metacritic = UNSET
    else:
      metacritic = RatingChild.from_dict(_metacritic)

    _rotten_tomatoes = d.pop("rottenTomatoes", UNSET)
    rotten_tomatoes: RatingChild | Unset
    if isinstance(_rotten_tomatoes, Unset):
      rotten_tomatoes = UNSET
    else:
      rotten_tomatoes = RatingChild.from_dict(_rotten_tomatoes)

    _trakt = d.pop("trakt", UNSET)
    trakt: RatingChild | Unset
    if isinstance(_trakt, Unset):
      trakt = UNSET
    else:
      trakt = RatingChild.from_dict(_trakt)

    ratings = cls(
      imdb=imdb,
      tmdb=tmdb,
      metacritic=metacritic,
      rotten_tomatoes=rotten_tomatoes,
      trakt=trakt,
    )

    return ratings
