from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credit_resource import CreditResource
from ...types import Response


def _get_kwargs(
  id: int,
) -> dict[str, Any]:

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/credit/{id}".format(
      id=quote(str(id), safe=""),
    ),
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreditResource | None:
  if response.status_code == 200:
    response_200 = CreditResource.from_dict(response.text)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreditResource]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  id: int,
  *,
  client: AuthenticatedClient | Client,
) -> Response[CreditResource]:
  """
  Args:
      id (int):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[CreditResource]
  """

  kwargs = _get_kwargs(
    id=id,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  id: int,
  *,
  client: AuthenticatedClient | Client,
) -> CreditResource | None:
  """
  Args:
      id (int):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      CreditResource
  """

  return sync_detailed(
    id=id,
    client=client,
  ).parsed


async def asyncio_detailed(
  id: int,
  *,
  client: AuthenticatedClient | Client,
) -> Response[CreditResource]:
  """
  Args:
      id (int):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[CreditResource]
  """

  kwargs = _get_kwargs(
    id=id,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  id: int,
  *,
  client: AuthenticatedClient | Client,
) -> CreditResource | None:
  """
  Args:
      id (int):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      CreditResource
  """

  return (
    await asyncio_detailed(
      id=id,
      client=client,
    )
  ).parsed
