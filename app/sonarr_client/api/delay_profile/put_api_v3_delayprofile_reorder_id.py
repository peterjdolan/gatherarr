from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delay_profile_resource import DelayProfileResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  id: int,
  *,
  after: int | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["after"] = after

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "put",
    "url": "/api/v3/delayprofile/reorder/{id}".format(
      id=quote(str(id), safe=""),
    ),
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[DelayProfileResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.text
    for response_200_item_data in _response_200:
      response_200_item = DelayProfileResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[DelayProfileResource]]:
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
  after: int | Unset = UNSET,
) -> Response[list[DelayProfileResource]]:
  """
  Args:
      id (int):
      after (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[DelayProfileResource]]
  """

  kwargs = _get_kwargs(
    id=id,
    after=after,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  id: int,
  *,
  client: AuthenticatedClient | Client,
  after: int | Unset = UNSET,
) -> list[DelayProfileResource] | None:
  """
  Args:
      id (int):
      after (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[DelayProfileResource]
  """

  return sync_detailed(
    id=id,
    client=client,
    after=after,
  ).parsed


async def asyncio_detailed(
  id: int,
  *,
  client: AuthenticatedClient | Client,
  after: int | Unset = UNSET,
) -> Response[list[DelayProfileResource]]:
  """
  Args:
      id (int):
      after (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[DelayProfileResource]]
  """

  kwargs = _get_kwargs(
    id=id,
    after=after,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  id: int,
  *,
  client: AuthenticatedClient | Client,
  after: int | Unset = UNSET,
) -> list[DelayProfileResource] | None:
  """
  Args:
      id (int):
      after (int | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[DelayProfileResource]
  """

  return (
    await asyncio_detailed(
      id=id,
      client=client,
      after=after,
    )
  ).parsed
