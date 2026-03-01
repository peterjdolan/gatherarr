import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.history_resource import HistoryResource
from ...models.movie_history_event_type import MovieHistoryEventType
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  date: datetime.datetime | Unset = UNSET,
  event_type: MovieHistoryEventType | Unset = UNSET,
  include_movie: bool | Unset = False,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  json_date: str | Unset = UNSET
  if not isinstance(date, Unset):
    json_date = date.isoformat()
  params["date"] = json_date

  json_event_type: str | Unset = UNSET
  if not isinstance(event_type, Unset):
    json_event_type = event_type.value

  params["eventType"] = json_event_type

  params["includeMovie"] = include_movie

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/history/since",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[HistoryResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.json()
    for response_200_item_data in _response_200:
      response_200_item = HistoryResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[HistoryResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  date: datetime.datetime | Unset = UNSET,
  event_type: MovieHistoryEventType | Unset = UNSET,
  include_movie: bool | Unset = False,
) -> Response[list[HistoryResource]]:
  """
  Args:
      date (datetime.datetime | Unset):
      event_type (MovieHistoryEventType | Unset):
      include_movie (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[HistoryResource]]
  """

  kwargs = _get_kwargs(
    date=date,
    event_type=event_type,
    include_movie=include_movie,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  date: datetime.datetime | Unset = UNSET,
  event_type: MovieHistoryEventType | Unset = UNSET,
  include_movie: bool | Unset = False,
) -> list[HistoryResource] | None:
  """
  Args:
      date (datetime.datetime | Unset):
      event_type (MovieHistoryEventType | Unset):
      include_movie (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[HistoryResource]
  """

  return sync_detailed(
    client=client,
    date=date,
    event_type=event_type,
    include_movie=include_movie,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  date: datetime.datetime | Unset = UNSET,
  event_type: MovieHistoryEventType | Unset = UNSET,
  include_movie: bool | Unset = False,
) -> Response[list[HistoryResource]]:
  """
  Args:
      date (datetime.datetime | Unset):
      event_type (MovieHistoryEventType | Unset):
      include_movie (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[HistoryResource]]
  """

  kwargs = _get_kwargs(
    date=date,
    event_type=event_type,
    include_movie=include_movie,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  date: datetime.datetime | Unset = UNSET,
  event_type: MovieHistoryEventType | Unset = UNSET,
  include_movie: bool | Unset = False,
) -> list[HistoryResource] | None:
  """
  Args:
      date (datetime.datetime | Unset):
      event_type (MovieHistoryEventType | Unset):
      include_movie (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[HistoryResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      date=date,
      event_type=event_type,
      include_movie=include_movie,
    )
  ).parsed
