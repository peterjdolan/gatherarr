from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.command_priority import CommandPriority
from ..models.command_result import CommandResult
from ..models.command_status import CommandStatus
from ..models.command_trigger import CommandTrigger
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.command import Command


T = TypeVar("T", bound="CommandResource")


@_attrs_define
class CommandResource:
  """
  Attributes:
      id (int | Unset):
      name (None | str | Unset):
      command_name (None | str | Unset):
      message (None | str | Unset):
      body (Command | Unset):
      priority (CommandPriority | Unset):
      status (CommandStatus | Unset):
      result (CommandResult | Unset):
      queued (datetime.datetime | Unset):
      started (datetime.datetime | None | Unset):
      ended (datetime.datetime | None | Unset):
      duration (None | str | Unset):
      exception (None | str | Unset):
      trigger (CommandTrigger | Unset):
      client_user_agent (None | str | Unset):
      state_change_time (datetime.datetime | None | Unset):
      send_updates_to_client (bool | Unset):
      update_scheduled_task (bool | Unset):
      last_execution_time (datetime.datetime | None | Unset):
  """

  id: int | Unset = UNSET
  name: None | str | Unset = UNSET
  command_name: None | str | Unset = UNSET
  message: None | str | Unset = UNSET
  body: Command | Unset = UNSET
  priority: CommandPriority | Unset = UNSET
  status: CommandStatus | Unset = UNSET
  result: CommandResult | Unset = UNSET
  queued: datetime.datetime | Unset = UNSET
  started: datetime.datetime | None | Unset = UNSET
  ended: datetime.datetime | None | Unset = UNSET
  duration: None | str | Unset = UNSET
  exception: None | str | Unset = UNSET
  trigger: CommandTrigger | Unset = UNSET
  client_user_agent: None | str | Unset = UNSET
  state_change_time: datetime.datetime | None | Unset = UNSET
  send_updates_to_client: bool | Unset = UNSET
  update_scheduled_task: bool | Unset = UNSET
  last_execution_time: datetime.datetime | None | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    name: None | str | Unset
    if isinstance(self.name, Unset):
      name = UNSET
    else:
      name = self.name

    command_name: None | str | Unset
    if isinstance(self.command_name, Unset):
      command_name = UNSET
    else:
      command_name = self.command_name

    message: None | str | Unset
    if isinstance(self.message, Unset):
      message = UNSET
    else:
      message = self.message

    body: dict[str, Any] | Unset = UNSET
    if not isinstance(self.body, Unset):
      body = self.body.to_dict()

    priority: str | Unset = UNSET
    if not isinstance(self.priority, Unset):
      priority = self.priority.value

    status: str | Unset = UNSET
    if not isinstance(self.status, Unset):
      status = self.status.value

    result: str | Unset = UNSET
    if not isinstance(self.result, Unset):
      result = self.result.value

    queued: str | Unset = UNSET
    if not isinstance(self.queued, Unset):
      queued = self.queued.isoformat()

    started: None | str | Unset
    if isinstance(self.started, Unset):
      started = UNSET
    elif isinstance(self.started, datetime.datetime):
      started = self.started.isoformat()
    else:
      started = self.started

    ended: None | str | Unset
    if isinstance(self.ended, Unset):
      ended = UNSET
    elif isinstance(self.ended, datetime.datetime):
      ended = self.ended.isoformat()
    else:
      ended = self.ended

    duration: None | str | Unset
    if isinstance(self.duration, Unset):
      duration = UNSET
    else:
      duration = self.duration

    exception: None | str | Unset
    if isinstance(self.exception, Unset):
      exception = UNSET
    else:
      exception = self.exception

    trigger: str | Unset = UNSET
    if not isinstance(self.trigger, Unset):
      trigger = self.trigger.value

    client_user_agent: None | str | Unset
    if isinstance(self.client_user_agent, Unset):
      client_user_agent = UNSET
    else:
      client_user_agent = self.client_user_agent

    state_change_time: None | str | Unset
    if isinstance(self.state_change_time, Unset):
      state_change_time = UNSET
    elif isinstance(self.state_change_time, datetime.datetime):
      state_change_time = self.state_change_time.isoformat()
    else:
      state_change_time = self.state_change_time

    send_updates_to_client = self.send_updates_to_client

    update_scheduled_task = self.update_scheduled_task

    last_execution_time: None | str | Unset
    if isinstance(self.last_execution_time, Unset):
      last_execution_time = UNSET
    elif isinstance(self.last_execution_time, datetime.datetime):
      last_execution_time = self.last_execution_time.isoformat()
    else:
      last_execution_time = self.last_execution_time

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if name is not UNSET:
      field_dict["name"] = name
    if command_name is not UNSET:
      field_dict["commandName"] = command_name
    if message is not UNSET:
      field_dict["message"] = message
    if body is not UNSET:
      field_dict["body"] = body
    if priority is not UNSET:
      field_dict["priority"] = priority
    if status is not UNSET:
      field_dict["status"] = status
    if result is not UNSET:
      field_dict["result"] = result
    if queued is not UNSET:
      field_dict["queued"] = queued
    if started is not UNSET:
      field_dict["started"] = started
    if ended is not UNSET:
      field_dict["ended"] = ended
    if duration is not UNSET:
      field_dict["duration"] = duration
    if exception is not UNSET:
      field_dict["exception"] = exception
    if trigger is not UNSET:
      field_dict["trigger"] = trigger
    if client_user_agent is not UNSET:
      field_dict["clientUserAgent"] = client_user_agent
    if state_change_time is not UNSET:
      field_dict["stateChangeTime"] = state_change_time
    if send_updates_to_client is not UNSET:
      field_dict["sendUpdatesToClient"] = send_updates_to_client
    if update_scheduled_task is not UNSET:
      field_dict["updateScheduledTask"] = update_scheduled_task
    if last_execution_time is not UNSET:
      field_dict["lastExecutionTime"] = last_execution_time

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.command import Command

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    name = _parse_name(d.pop("name", UNSET))

    def _parse_command_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    command_name = _parse_command_name(d.pop("commandName", UNSET))

    def _parse_message(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    message = _parse_message(d.pop("message", UNSET))

    _body = d.pop("body", UNSET)
    body: Command | Unset
    if isinstance(_body, Unset):
      body = UNSET
    else:
      body = Command.from_dict(_body)

    _priority = d.pop("priority", UNSET)
    priority: CommandPriority | Unset
    if isinstance(_priority, Unset):
      priority = UNSET
    else:
      priority = CommandPriority(_priority)

    _status = d.pop("status", UNSET)
    status: CommandStatus | Unset
    if isinstance(_status, Unset):
      status = UNSET
    else:
      status = CommandStatus(_status)

    _result = d.pop("result", UNSET)
    result: CommandResult | Unset
    if isinstance(_result, Unset):
      result = UNSET
    else:
      result = CommandResult(_result)

    _queued = d.pop("queued", UNSET)
    queued: datetime.datetime | Unset
    if isinstance(_queued, Unset):
      queued = UNSET
    else:
      queued = isoparse(_queued)

    def _parse_started(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        started_type_0 = isoparse(data)

        return started_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    started = _parse_started(d.pop("started", UNSET))

    def _parse_ended(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        ended_type_0 = isoparse(data)

        return ended_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    ended = _parse_ended(d.pop("ended", UNSET))

    def _parse_duration(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    duration = _parse_duration(d.pop("duration", UNSET))

    def _parse_exception(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    exception = _parse_exception(d.pop("exception", UNSET))

    _trigger = d.pop("trigger", UNSET)
    trigger: CommandTrigger | Unset
    if isinstance(_trigger, Unset):
      trigger = UNSET
    else:
      trigger = CommandTrigger(_trigger)

    def _parse_client_user_agent(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    client_user_agent = _parse_client_user_agent(d.pop("clientUserAgent", UNSET))

    def _parse_state_change_time(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        state_change_time_type_0 = isoparse(data)

        return state_change_time_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    state_change_time = _parse_state_change_time(d.pop("stateChangeTime", UNSET))

    send_updates_to_client = d.pop("sendUpdatesToClient", UNSET)

    update_scheduled_task = d.pop("updateScheduledTask", UNSET)

    def _parse_last_execution_time(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        last_execution_time_type_0 = isoparse(data)

        return last_execution_time_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    last_execution_time = _parse_last_execution_time(d.pop("lastExecutionTime", UNSET))

    command_resource = cls(
      id=id,
      name=name,
      command_name=command_name,
      message=message,
      body=body,
      priority=priority,
      status=status,
      result=result,
      queued=queued,
      started=started,
      ended=ended,
      duration=duration,
      exception=exception,
      trigger=trigger,
      client_user_agent=client_user_agent,
      state_change_time=state_change_time,
      send_updates_to_client=send_updates_to_client,
      update_scheduled_task=update_scheduled_task,
      last_execution_time=last_execution_time,
    )

    return command_resource
