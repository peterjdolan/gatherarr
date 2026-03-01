from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.movie_resource import MovieResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  imdb_id: str | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["imdbId"] = imdb_id

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/movie/lookup/imdb",
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
  imdb_id: str | Unset = UNSET,
) -> Response[MovieResource]:
  """
  Args:
      imdb_id (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MovieResource]
  """

  kwargs = _get_kwargs(
    imdb_id=imdb_id,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  imdb_id: str | Unset = UNSET,
) -> MovieResource | None:
  """
  Args:
      imdb_id (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MovieResource
  """

  return sync_detailed(
    client=client,
    imdb_id=imdb_id,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  imdb_id: str | Unset = UNSET,
) -> Response[MovieResource]:
  """
  Args:
      imdb_id (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MovieResource]
  """

  kwargs = _get_kwargs(
    imdb_id=imdb_id,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  imdb_id: str | Unset = UNSET,
) -> MovieResource | None:
  """
  Args:
      imdb_id (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MovieResource
  """

  return (
    await asyncio_detailed(
      client=client,
      imdb_id=imdb_id,
    )
  ).parsed
