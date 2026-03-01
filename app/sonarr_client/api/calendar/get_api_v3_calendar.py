import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.episode_resource import EpisodeResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  start: datetime.datetime | Unset = UNSET,
  end: datetime.datetime | Unset = UNSET,
  unmonitored: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode_file: bool | Unset = False,
  include_episode_images: bool | Unset = False,
  tags: str | Unset = "",
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  json_start: str | Unset = UNSET
  if not isinstance(start, Unset):
    json_start = start.isoformat()
  params["start"] = json_start

  json_end: str | Unset = UNSET
  if not isinstance(end, Unset):
    json_end = end.isoformat()
  params["end"] = json_end

  params["unmonitored"] = unmonitored

  params["includeSeries"] = include_series

  params["includeEpisodeFile"] = include_episode_file

  params["includeEpisodeImages"] = include_episode_images

  params["tags"] = tags

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/calendar",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[EpisodeResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.json()
    for response_200_item_data in _response_200:
      response_200_item = EpisodeResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[EpisodeResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  start: datetime.datetime | Unset = UNSET,
  end: datetime.datetime | Unset = UNSET,
  unmonitored: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode_file: bool | Unset = False,
  include_episode_images: bool | Unset = False,
  tags: str | Unset = "",
) -> Response[list[EpisodeResource]]:
  """
  Args:
      start (datetime.datetime | Unset):
      end (datetime.datetime | Unset):
      unmonitored (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode_file (bool | Unset):  Default: False.
      include_episode_images (bool | Unset):  Default: False.
      tags (str | Unset):  Default: ''.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[EpisodeResource]]
  """

  kwargs = _get_kwargs(
    start=start,
    end=end,
    unmonitored=unmonitored,
    include_series=include_series,
    include_episode_file=include_episode_file,
    include_episode_images=include_episode_images,
    tags=tags,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  start: datetime.datetime | Unset = UNSET,
  end: datetime.datetime | Unset = UNSET,
  unmonitored: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode_file: bool | Unset = False,
  include_episode_images: bool | Unset = False,
  tags: str | Unset = "",
) -> list[EpisodeResource] | None:
  """
  Args:
      start (datetime.datetime | Unset):
      end (datetime.datetime | Unset):
      unmonitored (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode_file (bool | Unset):  Default: False.
      include_episode_images (bool | Unset):  Default: False.
      tags (str | Unset):  Default: ''.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[EpisodeResource]
  """

  return sync_detailed(
    client=client,
    start=start,
    end=end,
    unmonitored=unmonitored,
    include_series=include_series,
    include_episode_file=include_episode_file,
    include_episode_images=include_episode_images,
    tags=tags,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  start: datetime.datetime | Unset = UNSET,
  end: datetime.datetime | Unset = UNSET,
  unmonitored: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode_file: bool | Unset = False,
  include_episode_images: bool | Unset = False,
  tags: str | Unset = "",
) -> Response[list[EpisodeResource]]:
  """
  Args:
      start (datetime.datetime | Unset):
      end (datetime.datetime | Unset):
      unmonitored (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode_file (bool | Unset):  Default: False.
      include_episode_images (bool | Unset):  Default: False.
      tags (str | Unset):  Default: ''.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[EpisodeResource]]
  """

  kwargs = _get_kwargs(
    start=start,
    end=end,
    unmonitored=unmonitored,
    include_series=include_series,
    include_episode_file=include_episode_file,
    include_episode_images=include_episode_images,
    tags=tags,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  start: datetime.datetime | Unset = UNSET,
  end: datetime.datetime | Unset = UNSET,
  unmonitored: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode_file: bool | Unset = False,
  include_episode_images: bool | Unset = False,
  tags: str | Unset = "",
) -> list[EpisodeResource] | None:
  """
  Args:
      start (datetime.datetime | Unset):
      end (datetime.datetime | Unset):
      unmonitored (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode_file (bool | Unset):  Default: False.
      include_episode_images (bool | Unset):  Default: False.
      tags (str | Unset):  Default: ''.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[EpisodeResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      start=start,
      end=end,
      unmonitored=unmonitored,
      include_series=include_series,
      include_episode_file=include_episode_file,
      include_episode_images=include_episode_images,
      tags=tags,
    )
  ).parsed
