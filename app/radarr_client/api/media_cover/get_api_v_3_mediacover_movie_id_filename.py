from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
  movie_id: int,
  filename: str,
) -> dict[str, Any]:

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/mediacover/{movie_id}/{filename}".format(
      movie_id=quote(str(movie_id), safe=""),
      filename=quote(str(filename), safe=""),
    ),
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
  if response.status_code == 200:
    return None

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  movie_id: int,
  filename: str,
  *,
  client: AuthenticatedClient | Client,
) -> Response[Any]:
  """
  Args:
      movie_id (int):
      filename (str):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
    filename=filename,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


async def asyncio_detailed(
  movie_id: int,
  filename: str,
  *,
  client: AuthenticatedClient | Client,
) -> Response[Any]:
  """
  Args:
      movie_id (int):
      filename (str):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    movie_id=movie_id,
    filename=filename,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)
