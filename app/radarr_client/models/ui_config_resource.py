from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.movie_runtime_format_type import MovieRuntimeFormatType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UiConfigResource")


@_attrs_define
class UiConfigResource:
  """
  Attributes:
      id (int | Unset):
      first_day_of_week (int | Unset):
      calendar_week_column_header (None | str | Unset):
      movie_runtime_format (MovieRuntimeFormatType | Unset):
      short_date_format (None | str | Unset):
      long_date_format (None | str | Unset):
      time_format (None | str | Unset):
      show_relative_dates (bool | Unset):
      enable_color_impaired_mode (bool | Unset):
      movie_info_language (int | Unset):
      ui_language (int | Unset):
      theme (None | str | Unset):
  """

  id: int | Unset = UNSET
  first_day_of_week: int | Unset = UNSET
  calendar_week_column_header: None | str | Unset = UNSET
  movie_runtime_format: MovieRuntimeFormatType | Unset = UNSET
  short_date_format: None | str | Unset = UNSET
  long_date_format: None | str | Unset = UNSET
  time_format: None | str | Unset = UNSET
  show_relative_dates: bool | Unset = UNSET
  enable_color_impaired_mode: bool | Unset = UNSET
  movie_info_language: int | Unset = UNSET
  ui_language: int | Unset = UNSET
  theme: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    first_day_of_week = self.first_day_of_week

    calendar_week_column_header: None | str | Unset
    if isinstance(self.calendar_week_column_header, Unset):
      calendar_week_column_header = UNSET
    else:
      calendar_week_column_header = self.calendar_week_column_header

    movie_runtime_format: str | Unset = UNSET
    if not isinstance(self.movie_runtime_format, Unset):
      movie_runtime_format = self.movie_runtime_format.value

    short_date_format: None | str | Unset
    if isinstance(self.short_date_format, Unset):
      short_date_format = UNSET
    else:
      short_date_format = self.short_date_format

    long_date_format: None | str | Unset
    if isinstance(self.long_date_format, Unset):
      long_date_format = UNSET
    else:
      long_date_format = self.long_date_format

    time_format: None | str | Unset
    if isinstance(self.time_format, Unset):
      time_format = UNSET
    else:
      time_format = self.time_format

    show_relative_dates = self.show_relative_dates

    enable_color_impaired_mode = self.enable_color_impaired_mode

    movie_info_language = self.movie_info_language

    ui_language = self.ui_language

    theme: None | str | Unset
    if isinstance(self.theme, Unset):
      theme = UNSET
    else:
      theme = self.theme

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if first_day_of_week is not UNSET:
      field_dict["firstDayOfWeek"] = first_day_of_week
    if calendar_week_column_header is not UNSET:
      field_dict["calendarWeekColumnHeader"] = calendar_week_column_header
    if movie_runtime_format is not UNSET:
      field_dict["movieRuntimeFormat"] = movie_runtime_format
    if short_date_format is not UNSET:
      field_dict["shortDateFormat"] = short_date_format
    if long_date_format is not UNSET:
      field_dict["longDateFormat"] = long_date_format
    if time_format is not UNSET:
      field_dict["timeFormat"] = time_format
    if show_relative_dates is not UNSET:
      field_dict["showRelativeDates"] = show_relative_dates
    if enable_color_impaired_mode is not UNSET:
      field_dict["enableColorImpairedMode"] = enable_color_impaired_mode
    if movie_info_language is not UNSET:
      field_dict["movieInfoLanguage"] = movie_info_language
    if ui_language is not UNSET:
      field_dict["uiLanguage"] = ui_language
    if theme is not UNSET:
      field_dict["theme"] = theme

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    first_day_of_week = d.pop("firstDayOfWeek", UNSET)

    def _parse_calendar_week_column_header(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    calendar_week_column_header = _parse_calendar_week_column_header(
      d.pop("calendarWeekColumnHeader", UNSET)
    )

    _movie_runtime_format = d.pop("movieRuntimeFormat", UNSET)
    movie_runtime_format: MovieRuntimeFormatType | Unset
    if isinstance(_movie_runtime_format, Unset):
      movie_runtime_format = UNSET
    else:
      movie_runtime_format = MovieRuntimeFormatType(_movie_runtime_format)

    def _parse_short_date_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    short_date_format = _parse_short_date_format(d.pop("shortDateFormat", UNSET))

    def _parse_long_date_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    long_date_format = _parse_long_date_format(d.pop("longDateFormat", UNSET))

    def _parse_time_format(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    time_format = _parse_time_format(d.pop("timeFormat", UNSET))

    show_relative_dates = d.pop("showRelativeDates", UNSET)

    enable_color_impaired_mode = d.pop("enableColorImpairedMode", UNSET)

    movie_info_language = d.pop("movieInfoLanguage", UNSET)

    ui_language = d.pop("uiLanguage", UNSET)

    def _parse_theme(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    theme = _parse_theme(d.pop("theme", UNSET))

    ui_config_resource = cls(
      id=id,
      first_day_of_week=first_day_of_week,
      calendar_week_column_header=calendar_week_column_header,
      movie_runtime_format=movie_runtime_format,
      short_date_format=short_date_format,
      long_date_format=long_date_format,
      time_format=time_format,
      show_relative_dates=show_relative_dates,
      enable_color_impaired_mode=enable_color_impaired_mode,
      movie_info_language=movie_info_language,
      ui_language=ui_language,
      theme=theme,
    )

    return ui_config_resource
