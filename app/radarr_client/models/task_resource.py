from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskResource")


@_attrs_define
class TaskResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      task_name (None | str | Unset):
      interval (int | Unset):
      last_execution (datetime.datetime | Unset):
      last_start_time (datetime.datetime | Unset):
      next_execution (datetime.datetime | Unset):
      last_duration (str | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  task_name: None | str | Unset = UNSET
  interval: int | Unset = UNSET
  last_execution: datetime.datetime | Unset = UNSET
  last_start_time: datetime.datetime | Unset = UNSET
  next_execution: datetime.datetime | Unset = UNSET
  last_duration: str | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    task_name: None | str | Unset
    if isinstance(self.task_name, Unset):
      task_name = UNSET
    else:
      task_name = self.task_name

    interval = self.interval

    last_execution: str | Unset = UNSET
    if not isinstance(self.last_execution, Unset):
      last_execution = self.last_execution.isoformat()

    last_start_time: str | Unset = UNSET
    if not isinstance(self.last_start_time, Unset):
      last_start_time = self.last_start_time.isoformat()

    next_execution: str | Unset = UNSET
    if not isinstance(self.next_execution, Unset):
      next_execution = self.next_execution.isoformat()

    last_duration = self.last_duration

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if task_name is not UNSET:
      field_dict["taskName"] = task_name
    if interval is not UNSET:
      field_dict["interval"] = interval
    if last_execution is not UNSET:
      field_dict["lastExecution"] = last_execution
    if last_start_time is not UNSET:
      field_dict["lastStartTime"] = last_start_time
    if next_execution is not UNSET:
      field_dict["nextExecution"] = next_execution
    if last_duration is not UNSET:
      field_dict["lastDuration"] = last_duration

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    def _parse_task_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    task_name = _parse_task_name(d.pop("taskName", UNSET))

    interval = d.pop("interval", UNSET)

    _last_execution = d.pop("lastExecution", UNSET)
    last_execution: datetime.datetime | Unset
    if isinstance(_last_execution, Unset):
      last_execution = UNSET
    else:
      last_execution = isoparse(_last_execution)

    _last_start_time = d.pop("lastStartTime", UNSET)
    last_start_time: datetime.datetime | Unset
    if isinstance(_last_start_time, Unset):
      last_start_time = UNSET
    else:
      last_start_time = isoparse(_last_start_time)

    _next_execution = d.pop("nextExecution", UNSET)
    next_execution: datetime.datetime | Unset
    if isinstance(_next_execution, Unset):
      next_execution = UNSET
    else:
      next_execution = isoparse(_next_execution)

    last_duration = d.pop("lastDuration", UNSET)

    task_resource = cls(
      id=id,
      name=name,
      task_name=task_name,
      interval=interval,
      last_execution=last_execution,
      last_start_time=last_start_time,
      next_execution=next_execution,
      last_duration=last_duration,
    )

    return task_resource
