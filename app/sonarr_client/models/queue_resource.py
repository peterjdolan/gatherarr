from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.download_protocol import DownloadProtocol
from ..models.queue_status import QueueStatus
from ..models.tracked_download_state import TrackedDownloadState
from ..models.tracked_download_status import TrackedDownloadStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.custom_format_resource import CustomFormatResource
  from ..models.episode_resource import EpisodeResource
  from ..models.language import Language
  from ..models.quality_model import QualityModel
  from ..models.series_resource import SeriesResource
  from ..models.tracked_download_status_message import TrackedDownloadStatusMessage


T = TypeVar("T", bound="QueueResource")


@_attrs_define
class QueueResource:
  """
  Attributes:
      id (int | Unset):
      series_id (int | None | Unset):
      episode_id (int | None | Unset):
      season_number (int | None | Unset):
      series (SeriesResource | Unset):
      episode (EpisodeResource | Unset):
      languages (list[Language] | None | Unset):
      quality (QualityModel | Unset):
      custom_formats (list[CustomFormatResource] | None | Unset):
      custom_format_score (int | Unset):
      size (float | Unset):
      title (None | str | Unset):
      estimated_completion_time (datetime.datetime | None | Unset):
      added (datetime.datetime | None | Unset):
      status (QueueStatus | Unset):
      tracked_download_status (TrackedDownloadStatus | Unset):
      tracked_download_state (TrackedDownloadState | Unset):
      status_messages (list[TrackedDownloadStatusMessage] | None | Unset):
      error_message (None | str | Unset):
      download_id (None | str | Unset):
      protocol (DownloadProtocol | Unset):
      download_client (None | str | Unset):
      download_client_has_post_import_category (bool | Unset):
      indexer (None | str | Unset):
      output_path (None | str | Unset):
      episode_has_file (bool | Unset):
      sizeleft (float | Unset):
      timeleft (None | str | Unset):
  """

  id: int | Unset = UNSET
  series_id: int | None | Unset = UNSET
  episode_id: int | None | Unset = UNSET
  season_number: int | None | Unset = UNSET
  series: SeriesResource | Unset = UNSET
  episode: EpisodeResource | Unset = UNSET
  languages: list[Language] | None | Unset = UNSET
  quality: QualityModel | Unset = UNSET
  custom_formats: list[CustomFormatResource] | None | Unset = UNSET
  custom_format_score: int | Unset = UNSET
  size: float | Unset = UNSET
  title: None | str | Unset = UNSET
  estimated_completion_time: datetime.datetime | None | Unset = UNSET
  added: datetime.datetime | None | Unset = UNSET
  status: QueueStatus | Unset = UNSET
  tracked_download_status: TrackedDownloadStatus | Unset = UNSET
  tracked_download_state: TrackedDownloadState | Unset = UNSET
  status_messages: list[TrackedDownloadStatusMessage] | None | Unset = UNSET
  error_message: None | str | Unset = UNSET
  download_id: None | str | Unset = UNSET
  protocol: DownloadProtocol | Unset = UNSET
  download_client: None | str | Unset = UNSET
  download_client_has_post_import_category: bool | Unset = UNSET
  indexer: None | str | Unset = UNSET
  output_path: None | str | Unset = UNSET
  episode_has_file: bool | Unset = UNSET
  sizeleft: float | Unset = UNSET
  timeleft: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    series_id: int | None | Unset
    if isinstance(self.series_id, Unset):
      series_id = UNSET
    else:
      series_id = self.series_id

    episode_id: int | None | Unset
    if isinstance(self.episode_id, Unset):
      episode_id = UNSET
    else:
      episode_id = self.episode_id

    season_number: int | None | Unset
    if isinstance(self.season_number, Unset):
      season_number = UNSET
    else:
      season_number = self.season_number

    series: dict[str, Any] | Unset = UNSET
    if not isinstance(self.series, Unset):
      series = self.series.to_dict()

    episode: dict[str, Any] | Unset = UNSET
    if not isinstance(self.episode, Unset):
      episode = self.episode.to_dict()

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

    size = self.size

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    estimated_completion_time: None | str | Unset
    if isinstance(self.estimated_completion_time, Unset):
      estimated_completion_time = UNSET
    elif isinstance(self.estimated_completion_time, datetime.datetime):
      estimated_completion_time = self.estimated_completion_time.isoformat()
    else:
      estimated_completion_time = self.estimated_completion_time

    added: None | str | Unset
    if isinstance(self.added, Unset):
      added = UNSET
    elif isinstance(self.added, datetime.datetime):
      added = self.added.isoformat()
    else:
      added = self.added

    status: str | Unset = UNSET
    if not isinstance(self.status, Unset):
      status = self.status.value

    tracked_download_status: str | Unset = UNSET
    if not isinstance(self.tracked_download_status, Unset):
      tracked_download_status = self.tracked_download_status.value

    tracked_download_state: str | Unset = UNSET
    if not isinstance(self.tracked_download_state, Unset):
      tracked_download_state = self.tracked_download_state.value

    status_messages: list[dict[str, Any]] | None | Unset
    if isinstance(self.status_messages, Unset):
      status_messages = UNSET
    elif isinstance(self.status_messages, list):
      status_messages = []
      for status_messages_type_0_item_data in self.status_messages:
        status_messages_type_0_item = status_messages_type_0_item_data.to_dict()
        status_messages.append(status_messages_type_0_item)

    else:
      status_messages = self.status_messages

    error_message: None | str | Unset
    if isinstance(self.error_message, Unset):
      error_message = UNSET
    else:
      error_message = self.error_message

    download_id: None | str | Unset
    if isinstance(self.download_id, Unset):
      download_id = UNSET
    else:
      download_id = self.download_id

    protocol: str | Unset = UNSET
    if not isinstance(self.protocol, Unset):
      protocol = self.protocol.value

    download_client: None | str | Unset
    if isinstance(self.download_client, Unset):
      download_client = UNSET
    else:
      download_client = self.download_client

    download_client_has_post_import_category = self.download_client_has_post_import_category

    indexer: None | str | Unset
    if isinstance(self.indexer, Unset):
      indexer = UNSET
    else:
      indexer = self.indexer

    output_path: None | str | Unset
    if isinstance(self.output_path, Unset):
      output_path = UNSET
    else:
      output_path = self.output_path

    episode_has_file = self.episode_has_file

    sizeleft = self.sizeleft

    timeleft: None | str | Unset
    if isinstance(self.timeleft, Unset):
      timeleft = UNSET
    else:
      timeleft = self.timeleft

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if series_id is not UNSET:
      field_dict["seriesId"] = series_id
    if episode_id is not UNSET:
      field_dict["episodeId"] = episode_id
    if season_number is not UNSET:
      field_dict["seasonNumber"] = season_number
    if series is not UNSET:
      field_dict["series"] = series
    if episode is not UNSET:
      field_dict["episode"] = episode
    if languages is not UNSET:
      field_dict["languages"] = languages
    if quality is not UNSET:
      field_dict["quality"] = quality
    if custom_formats is not UNSET:
      field_dict["customFormats"] = custom_formats
    if custom_format_score is not UNSET:
      field_dict["customFormatScore"] = custom_format_score
    if size is not UNSET:
      field_dict["size"] = size
    if title is not UNSET:
      field_dict["title"] = title
    if estimated_completion_time is not UNSET:
      field_dict["estimatedCompletionTime"] = estimated_completion_time
    if added is not UNSET:
      field_dict["added"] = added
    if status is not UNSET:
      field_dict["status"] = status
    if tracked_download_status is not UNSET:
      field_dict["trackedDownloadStatus"] = tracked_download_status
    if tracked_download_state is not UNSET:
      field_dict["trackedDownloadState"] = tracked_download_state
    if status_messages is not UNSET:
      field_dict["statusMessages"] = status_messages
    if error_message is not UNSET:
      field_dict["errorMessage"] = error_message
    if download_id is not UNSET:
      field_dict["downloadId"] = download_id
    if protocol is not UNSET:
      field_dict["protocol"] = protocol
    if download_client is not UNSET:
      field_dict["downloadClient"] = download_client
    if download_client_has_post_import_category is not UNSET:
      field_dict["downloadClientHasPostImportCategory"] = download_client_has_post_import_category
    if indexer is not UNSET:
      field_dict["indexer"] = indexer
    if output_path is not UNSET:
      field_dict["outputPath"] = output_path
    if episode_has_file is not UNSET:
      field_dict["episodeHasFile"] = episode_has_file
    if sizeleft is not UNSET:
      field_dict["sizeleft"] = sizeleft
    if timeleft is not UNSET:
      field_dict["timeleft"] = timeleft

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.custom_format_resource import CustomFormatResource
    from ..models.episode_resource import EpisodeResource
    from ..models.language import Language
    from ..models.quality_model import QualityModel
    from ..models.series_resource import SeriesResource
    from ..models.tracked_download_status_message import TrackedDownloadStatusMessage

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_series_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    series_id = _parse_series_id(d.pop("seriesId", UNSET))

    def _parse_episode_id(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    episode_id = _parse_episode_id(d.pop("episodeId", UNSET))

    def _parse_season_number(data: object) -> int | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(int | None | Unset, data)

    season_number = _parse_season_number(d.pop("seasonNumber", UNSET))

    _series = d.pop("series", UNSET)
    series: SeriesResource | Unset
    if isinstance(_series, Unset):
      series = UNSET
    else:
      series = SeriesResource.from_dict(_series)

    _episode = d.pop("episode", UNSET)
    episode: EpisodeResource | Unset
    if isinstance(_episode, Unset):
      episode = UNSET
    else:
      episode = EpisodeResource.from_dict(_episode)

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

    size = d.pop("size", UNSET)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    def _parse_estimated_completion_time(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        estimated_completion_time_type_0 = isoparse(data)

        return estimated_completion_time_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    estimated_completion_time = _parse_estimated_completion_time(
      d.pop("estimatedCompletionTime", UNSET)
    )

    def _parse_added(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        added_type_0 = isoparse(data)

        return added_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    added = _parse_added(d.pop("added", UNSET))

    _status = d.pop("status", UNSET)
    status: QueueStatus | Unset
    if isinstance(_status, Unset):
      status = UNSET
    else:
      status = QueueStatus(_status)

    _tracked_download_status = d.pop("trackedDownloadStatus", UNSET)
    tracked_download_status: TrackedDownloadStatus | Unset
    if isinstance(_tracked_download_status, Unset):
      tracked_download_status = UNSET
    else:
      tracked_download_status = TrackedDownloadStatus(_tracked_download_status)

    _tracked_download_state = d.pop("trackedDownloadState", UNSET)
    tracked_download_state: TrackedDownloadState | Unset
    if isinstance(_tracked_download_state, Unset):
      tracked_download_state = UNSET
    else:
      tracked_download_state = TrackedDownloadState(_tracked_download_state)

    def _parse_status_messages(data: object) -> list[TrackedDownloadStatusMessage] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        status_messages_type_0 = []
        _status_messages_type_0 = data
        for status_messages_type_0_item_data in _status_messages_type_0:
          status_messages_type_0_item = TrackedDownloadStatusMessage.from_dict(
            status_messages_type_0_item_data
          )

          status_messages_type_0.append(status_messages_type_0_item)

        return status_messages_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[TrackedDownloadStatusMessage] | None | Unset, data)

    status_messages = _parse_status_messages(d.pop("statusMessages", UNSET))

    def _parse_error_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    error_message = _parse_error_message(d.pop("errorMessage", UNSET))

    def _parse_download_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_id = _parse_download_id(d.pop("downloadId", UNSET))

    _protocol = d.pop("protocol", UNSET)
    protocol: DownloadProtocol | Unset
    if isinstance(_protocol, Unset):
      protocol = UNSET
    else:
      protocol = DownloadProtocol(_protocol)

    def _parse_download_client(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    download_client = _parse_download_client(d.pop("downloadClient", UNSET))

    download_client_has_post_import_category = d.pop("downloadClientHasPostImportCategory", UNSET)

    def _parse_indexer(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    indexer = _parse_indexer(d.pop("indexer", UNSET))

    def _parse_output_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    output_path = _parse_output_path(d.pop("outputPath", UNSET))

    episode_has_file = d.pop("episodeHasFile", UNSET)

    sizeleft = d.pop("sizeleft", UNSET)

    def _parse_timeleft(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    timeleft = _parse_timeleft(d.pop("timeleft", UNSET))

    queue_resource = cls(
      id=id,
      series_id=series_id,
      episode_id=episode_id,
      season_number=season_number,
      series=series,
      episode=episode,
      languages=languages,
      quality=quality,
      custom_formats=custom_formats,
      custom_format_score=custom_format_score,
      size=size,
      title=title,
      estimated_completion_time=estimated_completion_time,
      added=added,
      status=status,
      tracked_download_status=tracked_download_status,
      tracked_download_state=tracked_download_state,
      status_messages=status_messages,
      error_message=error_message,
      download_id=download_id,
      protocol=protocol,
      download_client=download_client,
      download_client_has_post_import_category=download_client_has_post_import_category,
      indexer=indexer,
      output_path=output_path,
      episode_has_file=episode_has_file,
      sizeleft=sizeleft,
      timeleft=timeleft,
    )

    return queue_resource
