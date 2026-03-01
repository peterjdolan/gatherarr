from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.movie_resource import MovieResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  tmdb_id: int | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["tmdbId"] = tmdb_id

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/movie/lookup/tmdb",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MovieResource | None:
  if response.status_code == 200:
    response_200 = MovieResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MovieResource]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  tmdb_id: int | Unset = UNSET,
) -> Response[MovieResource]:
  """
  Args:
      tmdb_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MovieResource]
  """

  kwargs = _get_kwargs(
    tmdb_id=tmdb_id,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  tmdb_id: int | Unset = UNSET,
) -> MovieResource | None:
  """
  Args:
      tmdb_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MovieResource
  """

  return sync_detailed(
    client=client,
    tmdb_id=tmdb_id,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  tmdb_id: int | Unset = UNSET,
) -> Response[MovieResource]:
  """
  Args:
      tmdb_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MovieResource]
  """

  kwargs = _get_kwargs(
    tmdb_id=tmdb_id,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  tmdb_id: int | Unset = UNSET,
) -> MovieResource | None:
  """
  Args:
      tmdb_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MovieResource
  """

  return (
    await asyncio_detailed(
      client=client,
      tmdb_id=tmdb_id,
    )
  ).parsed
