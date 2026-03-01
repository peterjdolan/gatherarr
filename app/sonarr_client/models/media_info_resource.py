from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaInfoResource")


@_attrs_define
class MediaInfoResource:
  """
  Attributes:
      id (int | Unset):
      audio_bitrate (int | Unset):
      audio_channels (float | Unset):
      audio_codec (None | str | Unset):
      audio_languages (None | str | Unset):
      audio_stream_count (int | Unset):
      video_bit_depth (int | Unset):
      video_bitrate (int | Unset):
      video_codec (None | str | Unset):
      video_fps (float | Unset):
      video_dynamic_range (None | str | Unset):
      video_dynamic_range_type (None | str | Unset):
      resolution (None | str | Unset):
      run_time (None | str | Unset):
      scan_type (None | str | Unset):
      subtitles (None | str | Unset):
  """

  id: int | Unset = UNSET
  audio_bitrate: int | Unset = UNSET
  audio_channels: float | Unset = UNSET
  audio_codec: None | str | Unset = UNSET
  audio_languages: None | str | Unset = UNSET
  audio_stream_count: int | Unset = UNSET
  video_bit_depth: int | Unset = UNSET
  video_bitrate: int | Unset = UNSET
  video_codec: None | str | Unset = UNSET
  video_fps: float | Unset = UNSET
  video_dynamic_range: None | str | Unset = UNSET
  video_dynamic_range_type: None | str | Unset = UNSET
  resolution: None | str | Unset = UNSET
  run_time: None | str | Unset = UNSET
  scan_type: None | str | Unset = UNSET
  subtitles: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    audio_bitrate = self.audio_bitrate

    audio_channels = self.audio_channels

    audio_codec: None | str | Unset
    if isinstance(self.audio_codec, Unset):
      audio_codec = UNSET
    else:
      audio_codec = self.audio_codec

    audio_languages: None | str | Unset
    if isinstance(self.audio_languages, Unset):
      audio_languages = UNSET
    else:
      audio_languages = self.audio_languages

    audio_stream_count = self.audio_stream_count

    video_bit_depth = self.video_bit_depth

    video_bitrate = self.video_bitrate

    video_codec: None | str | Unset
    if isinstance(self.video_codec, Unset):
      video_codec = UNSET
    else:
      video_codec = self.video_codec

    video_fps = self.video_fps

    video_dynamic_range: None | str | Unset
    if isinstance(self.video_dynamic_range, Unset):
      video_dynamic_range = UNSET
    else:
      video_dynamic_range = self.video_dynamic_range

    video_dynamic_range_type: None | str | Unset
    if isinstance(self.video_dynamic_range_type, Unset):
      video_dynamic_range_type = UNSET
    else:
      video_dynamic_range_type = self.video_dynamic_range_type

    resolution: None | str | Unset
    if isinstance(self.resolution, Unset):
      resolution = UNSET
    else:
      resolution = self.resolution

    run_time: None | str | Unset
    if isinstance(self.run_time, Unset):
      run_time = UNSET
    else:
      run_time = self.run_time

    scan_type: None | str | Unset
    if isinstance(self.scan_type, Unset):
      scan_type = UNSET
    else:
      scan_type = self.scan_type

    subtitles: None | str | Unset
    if isinstance(self.subtitles, Unset):
      subtitles = UNSET
    else:
      subtitles = self.subtitles

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if audio_bitrate is not UNSET:
      field_dict["audioBitrate"] = audio_bitrate
    if audio_channels is not UNSET:
      field_dict["audioChannels"] = audio_channels
    if audio_codec is not UNSET:
      field_dict["audioCodec"] = audio_codec
    if audio_languages is not UNSET:
      field_dict["audioLanguages"] = audio_languages
    if audio_stream_count is not UNSET:
      field_dict["audioStreamCount"] = audio_stream_count
    if video_bit_depth is not UNSET:
      field_dict["videoBitDepth"] = video_bit_depth
    if video_bitrate is not UNSET:
      field_dict["videoBitrate"] = video_bitrate
    if video_codec is not UNSET:
      field_dict["videoCodec"] = video_codec
    if video_fps is not UNSET:
      field_dict["videoFps"] = video_fps
    if video_dynamic_range is not UNSET:
      field_dict["videoDynamicRange"] = video_dynamic_range
    if video_dynamic_range_type is not UNSET:
      field_dict["videoDynamicRangeType"] = video_dynamic_range_type
    if resolution is not UNSET:
      field_dict["resolution"] = resolution
    if run_time is not UNSET:
      field_dict["runTime"] = run_time
    if scan_type is not UNSET:
      field_dict["scanType"] = scan_type
    if subtitles is not UNSET:
      field_dict["subtitles"] = subtitles

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    audio_bitrate = d.pop("audioBitrate", UNSET)

    audio_channels = d.pop("audioChannels", UNSET)

    def _parse_audio_codec(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    audio_codec = _parse_audio_codec(d.pop("audioCodec", UNSET))

    def _parse_audio_languages(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    audio_languages = _parse_audio_languages(d.pop("audioLanguages", UNSET))

    audio_stream_count = d.pop("audioStreamCount", UNSET)

    video_bit_depth = d.pop("videoBitDepth", UNSET)

    video_bitrate = d.pop("videoBitrate", UNSET)

    def _parse_video_codec(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    video_codec = _parse_video_codec(d.pop("videoCodec", UNSET))

    video_fps = d.pop("videoFps", UNSET)

    def _parse_video_dynamic_range(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    video_dynamic_range = _parse_video_dynamic_range(d.pop("videoDynamicRange", UNSET))

    def _parse_video_dynamic_range_type(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    video_dynamic_range_type = _parse_video_dynamic_range_type(
      d.pop("videoDynamicRangeType", UNSET)
    )

    def _parse_resolution(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    resolution = _parse_resolution(d.pop("resolution", UNSET))

    def _parse_run_time(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    run_time = _parse_run_time(d.pop("runTime", UNSET))

    def _parse_scan_type(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    scan_type = _parse_scan_type(d.pop("scanType", UNSET))

    def _parse_subtitles(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    subtitles = _parse_subtitles(d.pop("subtitles", UNSET))

    media_info_resource = cls(
      id=id,
      audio_bitrate=audio_bitrate,
      audio_channels=audio_channels,
      audio_codec=audio_codec,
      audio_languages=audio_languages,
      audio_stream_count=audio_stream_count,
      video_bit_depth=video_bit_depth,
      video_bitrate=video_bitrate,
      video_codec=video_codec,
      video_fps=video_fps,
      video_dynamic_range=video_dynamic_range,
      video_dynamic_range_type=video_dynamic_range_type,
      resolution=resolution,
      run_time=run_time,
      scan_type=scan_type,
      subtitles=subtitles,
    )

    return media_info_resource
