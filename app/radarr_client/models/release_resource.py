from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.download_protocol import DownloadProtocol
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.language import Language
  from ..models.quality_model import QualityModel


T = TypeVar("T", bound="ReleaseResource")


@_attrs_define
class ReleaseResource:
  """
  Attributes:
      id (int | Unset):
      guid (None | str | Unset):
      quality (QualityModel | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      custom_format_score (int | Unset):
      quality_weight (int | Unset):
      age (int | Unset):
      age_hours (float | Unset):
      age_minutes (float | Unset):
      size (int | Unset):
      indexer_id (int | Unset):
      indexer (None | str | Unset):
      release_group (None | str | Unset):
      sub_group (None | str | Unset):
      release_hash (None | str | Unset):
      title (None | str | Unset):
      scene_source (bool | Unset):
      movie_titles (list[str] | None | Unset):
      languages (list[Language] | None | Unset):
      mapped_movie_id (int | None | Unset):
      approved (bool | Unset):
      temporarily_rejected (bool | Unset):
      rejected (bool | Unset):
      tmdb_id (int | Unset):
      imdb_id (int | Unset):
      rejections (list[str] | None | Unset):
      publish_date (datetime.datetime | Unset):
      comment_url (None | str | Unset):
      download_url (None | str | Unset):
      info_url (None | str | Unset):
      movie_requested (bool | Unset):
      download_allowed (bool | Unset):
      release_weight (int | Unset):
      edition (None | str | Unset):
      magnet_url (None | str | Unset):
      info_hash (None | str | Unset):
      seeders (int | None | Unset):
      leechers (int | None | Unset):
      protocol (DownloadProtocol | Unset):
      indexer_flags (Any | Unset):
      movie_id (int | None | Unset):
      download_client_id (int | None | Unset):
      download_client (None | str | Unset):
      should_override (bool | None | Unset):
  """

  id: int | Unset = UNSET
  guid: None | str | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  custom_format_score: int | Unset = UNSET
  quality_weight: int | Unset = UNSET
  age: int | Unset = UNSET
  age_hours: float | Unset = UNSET
  age_minutes: float | Unset = UNSET
  size: int | Unset = UNSET
  indexer_id: int | Unset = UNSET
  indexer: None | str | Unset = UNSET
  release_group: None | str | Unset = UNSET
  sub_group: None | str | Unset = UNSET
  release_hash: None | str | Unset = UNSET
  title: None | str | Unset = UNSET
  scene_source: bool | Unset = UNSET
  movie_titles: list[str] | None | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  mapped_movie_id: int | None | Unset = UNSET
  approved: bool | Unset = UNSET
  temporarily_rejected: bool | Unset = UNSET
  rejected: bool | Unset = UNSET
  tmdb_id: int | Unset = UNSET
  imdb_id: int | Unset = UNSET
  rejections: list[str] | None | Unset = UNSET
  publish_date: datetime.datetime | Unset = UNSET
  comment_url: None | str | Unset = UNSET
  download_url: None | str | Unset = UNSET
  info_url: None | str | Unset = UNSET
  movie_requested: bool | Unset = UNSET
  download_allowed: bool | Unset = UNSET
  release_weight: int | Unset = UNSET
  edition: None | str | Unset = UNSET
  magnet_url: None | str | Unset = UNSET
  info_hash: None | str | Unset = UNSET
  seeders: int | None | Unset = UNSET
  leechers: int | None | Unset = UNSET
  protocol: DownloadProtocol | Unset = UNSET
  indexer_flags: Any | Unset = UNSET
  movie_id: int | None | Unset = UNSET
  download_client_id: int | None | Unset = UNSET
  download_client: None | str | Unset = UNSET
  should_override: bool | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    guid: None | str | Unset
    if isinstance(self.guid, Unset):
      guid = UNSET
    else:
      guid = self.guid

    quality: dict[str, Any] | Unset = UNSET
    if not isinstance(self.quality, Unset):
      quality = self.quality.to_dict()

    custom_formats: list[dict[str, Any]] | None | Unset
    if isinstance(self.custom_formats, Unset):
      custom_formats = UNSET
    elif isinstance(self.custom_formats, list):
      custom_formats = []
      for custom_formats_type_0_item_data in self.custom_formats:
        custom_formats_type_0_item = custom_formats_type_0_item_data.to_dict()
        custom_formats.append(custom_formats_type_0_item)

    else:
      custom_formats = self.custom_formats

    custom_format_score = self.custom_format_score

    quality_weight = self.quality_weight

    age = self.age

    age_hours = self.age_hours

    age_minutes = self.age_minutes

    size = self.size

    indexer_id = self.indexer_id

    indexer: None | str | Unset
    if isinstance(self.indexer, Unset):
      indexer = UNSET
    else:
      indexer = self.indexer

    release_group: None | str | Unset
    if isinstance(self.release_group, Unset):
      release_group = UNSET
    else:
      release_group = self.release_group

    sub_group: None | str | Unset
    if isinstance(self.sub_group, Unset):
      sub_group = UNSET
    else:
      sub_group = self.sub_group

    release_hash: None | str | Unset
    if isinstance(self.release_hash, Unset):
      release_hash = UNSET
    else:
      release_hash = self.release_hash

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    scene_source = self.scene_source

    movie_titles: list[str] | None | Unset
    if isinstance(self.movie_titles, Unset):
      movie_titles = UNSET
    elif isinstance(self.movie_titles, list):
      movie_titles = self.movie_titles

    else:
      movie_titles = self.movie_titles

    languages: list[dict[str, Any]] | None | Unset
    if isinstance(self.languages, Unset):
      languages = UNSET
    elif isinstance(self.languages, list):
      languages = []
      for languages_type_0_item_data in self.languages:
        languages_type_0_item = languages_type_0_item_data.to_dict()
        languages.append(languages_type_0_item)

    else:
      languages = self.languages

    mapped_movie_id: int | None | Unset
    if isinstance(self.mapped_movie_id, Unset):
      mapped_movie_id = UNSET
    else:
      mapped_movie_id = self.mapped_movie_id

    approved = self.approved

    temporarily_rejected = self.temporarily_rejected

    rejected = self.rejected

    tmdb_id = self.tmdb_id

    imdb_id = self.imdb_id

    rejections: list[str] | None | Unset
    if isinstance(self.rejections, Unset):
      rejections = UNSET
    elif isinstance(self.rejections, list):
      rejections = self.rejections

    else:
      rejections = self.rejections

    publish_date: str | Unset = UNSET
    if not isinstance(self.publish_date, Unset):
      publish_date = self.publish_date.isoformat()

    comment_url: None | str | Unset
    if isinstance(self.comment_url, Unset):
      comment_url = UNSET
    else:
      comment_url = self.comment_url

    download_url: None | str | Unset
    if isinstance(self.download_url, Unset):
      download_url = UNSET
    else:
      download_url = self.download_url

    info_url: None | str | Unset
    if isinstance(self.info_url, Unset):
      info_url = UNSET
    else:
      info_url = self.info_url

    movie_requested = self.movie_requested

    download_allowed = self.download_allowed

    release_weight = self.release_weight

    edition: None | str | Unset
    if isinstance(self.edition, Unset):
      edition = UNSET
    else:
      edition = self.edition

    magnet_url: None | str | Unset
    if isinstance(self.magnet_url, Unset):
      magnet_url = UNSET
    else:
      magnet_url = self.magnet_url

    info_hash: None | str | Unset
    if isinstance(self.info_hash, Unset):
      info_hash = UNSET
    else:
      info_hash = self.info_hash

    seeders: int | None | Unset
    if isinstance(self.seeders, Unset):
      seeders = UNSET
    else:
      seeders = self.seeders

    leechers: int | None | Unset
    if isinstance(self.leechers, Unset):
      leechers = UNSET
    else:
      leechers = self.leechers

    protocol: str | Unset = UNSET
    if not isinstance(self.protocol, Unset):
      protocol = self.protocol.value

    indexer_flags = self.indexer_flags

    movie_id: int | None | Unset
    if isinstance(self.movie_id, Unset):
      movie_id = UNSET
    else:
      movie_id = self.movie_id

    download_client_id: int | None | Unset
    if isinstance(self.download_client_id, Unset):
      download_client_id = UNSET
    else:
      download_client_id = self.download_client_id

    download_client: None | str | Unset
    if isinstance(self.download_client, Unset):
      download_client = UNSET
    else:
      download_client = self.download_client

    should_override: bool | None | Unset
    if isinstance(self.should_override, Unset):
      should_override = UNSET
    else:
      should_override = self.should_override

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if guid is not UNSET:
      field_dict["guid"] = guid
    if quality is not UNSET:
      field_dict["quality"] = quality
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if custom_format_score is not UNSET:
      field_dict["customFormatScore"] = custom_format_score
    if quality_weight is not UNSET:
      field_dict["qualityWeight"] = quality_weight
    if age is not UNSET:
      field_dict["age"] = age
    if age_hours is not UNSET:
      field_dict["ageHours"] = age_hours
    if age_minutes is not UNSET:
      field_dict["ageMinutes"] = age_minutes
    if size is not UNSET:
      field_dict["size"] = size
    if indexer_id is not UNSET:
      field_dict["indexerId"] = indexer_id
    if indexer is not UNSET:
      field_dict["indexer"] = indexer
    if release_group is not UNSET:
      field_dict["releaseGroup"] = release_group
    if sub_group is not UNSET:
      field_dict["subGroup"] = sub_group
    if release_hash is not UNSET:
      field_dict["releaseHash"] = release_hash
    if title is not UNSET:
      field_dict["title"] = title
    if scene_source is not UNSET:
      field_dict["sceneSource"] = scene_source
    if movie_titles is not UNSET:
      field_dict["movieTitles"] = movie_titles
    if languages is not UNSET:
      field_dict["languages"] = languages
    if mapped_movie_id is not UNSET:
      field_dict["mappedMovieId"] = mapped_movie_id
    if approved is not UNSET:
      field_dict["approved"] = approved
    if temporarily_rejected is not UNSET:
      field_dict["temporarilyRejected"] = temporarily_rejected
    if rejected is not UNSET:
      field_dict["rejected"] = rejected
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id
    if imdb_id is not UNSET:
      field_dict["imdbId"] = imdb_id
    if rejections is not UNSET:
      field_dict["rejections"] = rejections
    if publish_date is not UNSET:
      field_dict["publishDate"] = publish_date
    if comment_url is not UNSET:
      field_dict["commentUrl"] = comment_url
    if download_url is not UNSET:
      field_dict["downloadUrl"] = download_url
    if info_url is not UNSET:
      field_dict["infoUrl"] = info_url
    if movie_requested is not UNSET:
      field_dict["movieRequested"] = movie_requested
    if download_allowed is not UNSET:
      field_dict["downloadAllowed"] = download_allowed
    if release_weight is not UNSET:
      field_dict["releaseWeight"] = release_weight
    if edition is not UNSET:
      field_dict["edition"] = edition
    if magnet_url is not UNSET:
      field_dict["magnetUrl"] = magnet_url
    if info_hash is not UNSET:
      field_dict["infoHash"] = info_hash
    if seeders is not UNSET:
      field_dict["seeders"] = seeders
    if leechers is not UNSET:
      field_dict["leechers"] = leechers
    if protocol is not UNSET:
      field_dict["protocol"] = protocol
    if indexer_flags is not UNSET:
      field_dict["indexerFlags"] = indexer_flags
    if movie_id is not UNSET:
      field_dict["movieId"] = movie_id
    if download_client_id is not UNSET:
      field_dict["downloadClientId"] = download_client_id
    if download_client is not UNSET:
      field_dict["downloadClient"] = download_client
    if should_override is not UNSET:
      field_dict["shouldOverride"] = should_override

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.language import Language
    from ..models.quality_model import QualityModel

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_guid(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    guid = _parse_guid(d.pop("guid", UNSET))

    _quality = d.pop("quality", UNSET)
    quality: QualityModel | Unset
    if isinstance(_quality, Unset):
      quality = UNSET
    else:
      quality = QualityModel.from_dict(_quality)

    def _parse_custom_formats(data: object) -> list[CustomFormatResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        custom_formats_type_0 = []
        _custom_formats_type_0 = data
        for custom_formats_type_0_item_data in _custom_formats_type_0:
          custom_formats_type_0_item = CustomFormatResource.from_dict(
            custom_formats_type_0_item_data
          )

          custom_formats_type_0.append(custom_formats_type_0_item)

        return custom_formats_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[CustomFormatResource] | None | Unset, data)

    custom_formats = _parse_custom_formats(d.pop("customFormats", UNSET))

    custom_format_score = d.pop("customFormatScore", UNSET)

    quality_weight = d.pop("qualityWeight", UNSET)

    age = d.pop("age", UNSET)

    age_hours = d.pop("ageHours", UNSET)

    age_minutes = d.pop("ageMinutes", UNSET)

    size = d.pop("size", UNSET)

    indexer_id = d.pop("indexerId", UNSET)

    def _parse_indexer(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    indexer = _parse_indexer(d.pop("indexer", UNSET))

    def _parse_release_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_group = _parse_release_group(d.pop("releaseGroup", UNSET))

    def _parse_sub_group(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sub_group = _parse_sub_group(d.pop("subGroup", UNSET))

    def _parse_release_hash(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    release_hash = _parse_release_hash(d.pop("releaseHash", UNSET))

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    scene_source = d.pop("sceneSource", UNSET)

    def _parse_movie_titles(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        movie_titles_type_0 = cast(list[str], data)

        return movie_titles_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    movie_titles = _parse_movie_titles(d.pop("movieTitles", UNSET))

    def _parse_languages(data: object) -> list[Language] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        languages_type_0 = []
        _languages_type_0 = data
        for languages_type_0_item_data in _languages_type_0:
          languages_type_0_item = Language.from_dict(languages_type_0_item_data)

          languages_type_0.append(languages_type_0_item)

        return languages_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[Language] | None | Unset, data)

    languages = _parse_languages(d.pop("languages", UNSET))

    def _parse_mapped_movie_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    mapped_movie_id = _parse_mapped_movie_id(d.pop("mappedMovieId", UNSET))

    approved = d.pop("approved", UNSET)

    temporarily_rejected = d.pop("temporarilyRejected", UNSET)

    rejected = d.pop("rejected", UNSET)

    tmdb_id = d.pop("tmdbId", UNSET)

    imdb_id = d.pop("imdbId", UNSET)

    def _parse_rejections(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        rejections_type_0 = cast(list[str], data)

        return rejections_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    rejections = _parse_rejections(d.pop("rejections", UNSET))

    _publish_date = d.pop("publishDate", UNSET)
    publish_date: datetime.datetime | Unset
    if isinstance(_publish_date, Unset):
      publish_date = UNSET
    else:
      publish_date = isoparse(_publish_date)

    def _parse_comment_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    comment_url = _parse_comment_url(d.pop("commentUrl", UNSET))

    def _parse_download_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_url = _parse_download_url(d.pop("downloadUrl", UNSET))

    def _parse_info_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    info_url = _parse_info_url(d.pop("infoUrl", UNSET))

    movie_requested = d.pop("movieRequested", UNSET)

    download_allowed = d.pop("downloadAllowed", UNSET)

    release_weight = d.pop("releaseWeight", UNSET)

    def _parse_edition(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    edition = _parse_edition(d.pop("edition", UNSET))

    def _parse_magnet_url(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    magnet_url = _parse_magnet_url(d.pop("magnetUrl", UNSET))

    def _parse_info_hash(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    info_hash = _parse_info_hash(d.pop("infoHash", UNSET))

    def _parse_seeders(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    seeders = _parse_seeders(d.pop("seeders", UNSET))

    def _parse_leechers(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    leechers = _parse_leechers(d.pop("leechers", UNSET))

    _protocol = d.pop("protocol", UNSET)
    protocol: DownloadProtocol | Unset
    if isinstance(_protocol, Unset):
      protocol = UNSET
    else:
      protocol = DownloadProtocol(_protocol)

    indexer_flags = d.pop("indexerFlags", UNSET)

    def _parse_movie_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    movie_id = _parse_movie_id(d.pop("movieId", UNSET))

    def _parse_download_client_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    download_client_id = _parse_download_client_id(d.pop("downloadClientId", UNSET))

    def _parse_download_client(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_client = _parse_download_client(d.pop("downloadClient", UNSET))

    def _parse_should_override(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    should_override = _parse_should_override(d.pop("shouldOverride", UNSET))

    release_resource = cls(
      id=id,
      guid=guid,
      quality=quality,
      custom_formats=custom_formats,
      custom_format_score=custom_format_score,
      quality_weight=quality_weight,
      age=age,
      age_hours=age_hours,
      age_minutes=age_minutes,
      size=size,
      indexer_id=indexer_id,
      indexer=indexer,
      release_group=release_group,
      sub_group=sub_group,
      release_hash=release_hash,
      title=title,
      scene_source=scene_source,
      movie_titles=movie_titles,
      languages=languages,
      mapped_movie_id=mapped_movie_id,
      approved=approved,
      temporarily_rejected=temporarily_rejected,
      rejected=rejected,
      tmdb_id=tmdb_id,
      imdb_id=imdb_id,
      rejections=rejections,
      publish_date=publish_date,
      comment_url=comment_url,
      download_url=download_url,
      info_url=info_url,
      movie_requested=movie_requested,
      download_allowed=download_allowed,
      release_weight=release_weight,
      edition=edition,
      magnet_url=magnet_url,
      info_hash=info_hash,
      seeders=seeders,
      leechers=leechers,
      protocol=protocol,
      indexer_flags=indexer_flags,
      movie_id=movie_id,
      download_client_id=download_client_id,
      download_client=download_client,
      should_override=should_override,
    )

    return release_resource
