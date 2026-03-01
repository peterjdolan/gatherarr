from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.episode_file_resource import EpisodeFileResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  series_id: int | Unset = UNSET,
  episode_file_ids: list[int] | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["seriesId"] = series_id

  json_episode_file_ids: list[int] | Unset = UNSET
  if not isinstance(episode_file_ids, Unset):
    json_episode_file_ids = episode_file_ids

  params["episodeFileIds"] = json_episode_file_ids

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/episodefile",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[EpisodeFileResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.json()
    for response_200_item_data in _response_200:
      response_200_item = EpisodeFileResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[EpisodeFileResource]]:
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
  episode_file_ids: list[int] | Unset = UNSET,
) -> Response[list[EpisodeFileResource]]:
  """
  Args:
      series_id (int | Unset):
      episode_file_ids (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[EpisodeFileResource]]
  """

  kwargs = _get_kwargs(
    series_id=series_id,
    episode_file_ids=episode_file_ids,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_file_ids: list[int] | Unset = UNSET,
) -> list[EpisodeFileResource] | None:
  """
  Args:
      series_id (int | Unset):
      episode_file_ids (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[EpisodeFileResource]
  """

  return sync_detailed(
    client=client,
    series_id=series_id,
    episode_file_ids=episode_file_ids,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_file_ids: list[int] | Unset = UNSET,
) -> Response[list[EpisodeFileResource]]:
  """
  Args:
      series_id (int | Unset):
      episode_file_ids (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[EpisodeFileResource]]
  """

  kwargs = _get_kwargs(
    series_id=series_id,
    episode_file_ids=episode_file_ids,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  series_id: int | Unset = UNSET,
  episode_file_ids: list[int] | Unset = UNSET,
) -> list[EpisodeFileResource] | None:
  """
  Args:
      series_id (int | Unset):
      episode_file_ids (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[EpisodeFileResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      series_id=series_id,
      episode_file_ids=episode_file_ids,
    )
  ).parsed
