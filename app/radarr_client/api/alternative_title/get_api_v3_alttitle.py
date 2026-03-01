from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.alternative_title_resource import AlternativeTitleResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  movie_id: int | Unset = UNSET,
  movie_metadata_id: int | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["movieId"] = movie_id

  params["movieMetadataId"] = movie_metadata_id

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/alttitle",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[AlternativeTitleResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.text
    for response_200_item_data in _response_200:
      response_200_item = AlternativeTitleResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[AlternativeTitleResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  movie_id: int | Unset = UNSET,
  movie_metadata_id: int | Unset = UNSET,
) -> Response[list[AlternativeTitleResource]]:
  """
  Args:
      movie_id (int | Unset):
      movie_metadata_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[AlternativeTitleResource]]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
    movie_metadata_id=movie_metadata_id,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  movie_id: int | Unset = UNSET,
  movie_metadata_id: int | Unset = UNSET,
) -> list[AlternativeTitleResource] | None:
  """
  Args:
      movie_id (int | Unset):
      movie_metadata_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[AlternativeTitleResource]
  """

  return sync_detailed(
    client=client,
    movie_id=movie_id,
    movie_metadata_id=movie_metadata_id,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  movie_id: int | Unset = UNSET,
  movie_metadata_id: int | Unset = UNSET,
) -> Response[list[AlternativeTitleResource]]:
  """
  Args:
      movie_id (int | Unset):
      movie_metadata_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[AlternativeTitleResource]]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
    movie_metadata_id=movie_metadata_id,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  movie_id: int | Unset = UNSET,
  movie_metadata_id: int | Unset = UNSET,
) -> list[AlternativeTitleResource] | None:
  """
  Args:
      movie_id (int | Unset):
      movie_metadata_id (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[AlternativeTitleResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      movie_id=movie_id,
      movie_metadata_id=movie_metadata_id,
    )
  ).parsed
