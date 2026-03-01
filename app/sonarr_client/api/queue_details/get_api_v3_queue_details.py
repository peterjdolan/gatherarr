from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.queue_resource import QueueResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  series_id: int | Unset = UNSET,
  episode_ids: list[int] | Unset = UNSET,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["seriesId"] = series_id

  json_episode_ids: list[int] | Unset = UNSET
  if not isinstance(episode_ids, Unset):
    json_episode_ids = episode_ids

  params["episodeIds"] = json_episode_ids

  params["includeSeries"] = include_series

  params["includeEpisode"] = include_episode

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/queue/details",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[QueueResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.json()
    for response_200_item_data in _response_200:
      response_200_item = QueueResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[QueueResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_ids: list[int] | Unset = UNSET,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
) -> Response[list[QueueResource]]:
  """
  Args:
      series_id (int | Unset):
      episode_ids (list[int] | Unset):
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[QueueResource]]
  """

  kwargs = _get_kwargs(
    series_id=series_id,
    episode_ids=episode_ids,
    include_series=include_series,
    include_episode=include_episode,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_ids: list[int] | Unset = UNSET,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
) -> list[QueueResource] | None:
  """
  Args:
      series_id (int | Unset):
      episode_ids (list[int] | Unset):
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[QueueResource]
  """

  return sync_detailed(
    client=client,
    series_id=series_id,
    episode_ids=episode_ids,
    include_series=include_series,
    include_episode=include_episode,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_ids: list[int] | Unset = UNSET,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
) -> Response[list[QueueResource]]:
  """
  Args:
      series_id (int | Unset):
      episode_ids (list[int] | Unset):
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[QueueResource]]
  """

  kwargs = _get_kwargs(
    series_id=series_id,
    episode_ids=episode_ids,
    include_series=include_series,
    include_episode=include_episode,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_ids: list[int] | Unset = UNSET,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
) -> list[QueueResource] | None:
  """
  Args:
      series_id (int | Unset):
      episode_ids (list[int] | Unset):
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[QueueResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      series_id=series_id,
      episode_ids=episode_ids,
      include_series=include_series,
      include_episode=include_episode,
    )
  ).parsed
