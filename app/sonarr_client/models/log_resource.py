from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogResource")


@_attrs_define
class LogResource:
  """
  Attributes:
      id (int | Unset):
      time (datetime.datetime | Unset):
      exception (None | str | Unset):
      exception_type (None | str | Unset):
      level (None | str | Unset):
      logger (None | str | Unset):
      message (None | str | Unset):
      method (None | str | Unset):
  """

  id: int | Unset = UNSET
  time: datetime.datetime | Unset = UNSET
  exception: None | str | Unset = UNSET
  exception_type: None | str | Unset = UNSET
  level: None | str | Unset = UNSET
  logger: None | str | Unset = UNSET
  message: None | str | Unset = UNSET
  method: None | str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    time: str | Unset = UNSET
    if not isinstance(self.time, Unset):
      time = self.time.isoformat()

    exception: None | str | Unset
    if isinstance(self.exception, Unset):
      exception = UNSET
    else:
      exception = self.exception

    exception_type: None | str | Unset
    if isinstance(self.exception_type, Unset):
      exception_type = UNSET
    else:
      exception_type = self.exception_type

    level: None | str | Unset
    if isinstance(self.level, Unset):
      level = UNSET
    else:
      level = self.level

    logger: None | str | Unset
    if isinstance(self.logger, Unset):
      logger = UNSET
    else:
      logger = self.logger

    message: None | str | Unset
    if isinstance(self.message, Unset):
      message = UNSET
    else:
      message = self.message

    method: None | str | Unset
    if isinstance(self.method, Unset):
      method = UNSET
    else:
      method = self.method

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if time is not UNSET:
      field_dict["time"] = time
    if exception is not UNSET:
      field_dict["exception"] = exception
    if exception_type is not UNSET:
      field_dict["exceptionType"] = exception_type
    if level is not UNSET:
      field_dict["level"] = level
    if logger is not UNSET:
      field_dict["logger"] = logger
    if message is not UNSET:
      field_dict["message"] = message
    if method is not UNSET:
      field_dict["method"] = method

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    _time = d.pop("time", UNSET)
    time: datetime.datetime | Unset
    if isinstance(_time, Unset):
      time = UNSET
    else:
      time = isoparse(_time)

    def _parse_exception(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    exception = _parse_exception(d.pop("exception", UNSET))

    def _parse_exception_type(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    exception_type = _parse_exception_type(d.pop("exceptionType", UNSET))

    def _parse_level(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    level = _parse_level(d.pop("level", UNSET))

    def _parse_logger(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    logger = _parse_logger(d.pop("logger", UNSET))

    def _parse_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    message = _parse_message(d.pop("message", UNSET))

    def _parse_method(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    method = _parse_method(d.pop("method", UNSET))

    log_resource = cls(
      id=id,
      time=time,
      exception=exception,
      exception_type=exception_type,
      level=level,
      logger=logger,
      message=message,
      method=method,
    )

    return log_resource
