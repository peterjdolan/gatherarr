from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rename_movie_resource import RenameMovieResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  movie_id: list[int] | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  json_movie_id: list[int] | Unset = UNSET
  if not isinstance(movie_id, Unset):
    json_movie_id = movie_id

  params["movieId"] = json_movie_id

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/rename",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[RenameMovieResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.text
    for response_200_item_data in _response_200:
      response_200_item = RenameMovieResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[RenameMovieResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  movie_id: list[int] | Unset = UNSET,
) -> Response[list[RenameMovieResource]]:
  """
  Args:
      movie_id (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[RenameMovieResource]]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  movie_id: list[int] | Unset = UNSET,
) -> list[RenameMovieResource] | None:
  """
  Args:
      movie_id (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[RenameMovieResource]
  """

  return sync_detailed(
    client=client,
    movie_id=movie_id,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  movie_id: list[int] | Unset = UNSET,
) -> Response[list[RenameMovieResource]]:
  """
  Args:
      movie_id (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[RenameMovieResource]]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  movie_id: list[int] | Unset = UNSET,
) -> list[RenameMovieResource] | None:
  """
  Args:
      movie_id (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[RenameMovieResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      movie_id=movie_id,
    )
  ).parsed
