from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
  id: int,
  *,
  remove_from_client: bool | Unset = True,
  blocklist: bool | Unset = False,
  skip_redownload: bool | Unset = False,
  change_category: bool | Unset = False,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["removeFromClient"] = remove_from_client

  params["blocklist"] = blocklist

  params["skipRedownload"] = skip_redownload

  params["changeCategory"] = change_category

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "delete",
    "url": "/api/v3/queue/{id}".format(
      id=quote(str(id), safe=""),
    ),
    "params": params,
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
  id: int,
  *,
  client: AuthenticatedClient | Client,
  remove_from_client: bool | Unset = True,
  blocklist: bool | Unset = False,
  skip_redownload: bool | Unset = False,
  change_category: bool | Unset = False,
) -> Response[Any]:
  """
  Args:
      id (int):
      remove_from_client (bool | Unset):  Default: True.
      blocklist (bool | Unset):  Default: False.
      skip_redownload (bool | Unset):  Default: False.
      change_category (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    id=id,
    remove_from_client=remove_from_client,
    blocklist=blocklist,
    skip_redownload=skip_redownload,
    change_category=change_category,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


async def asyncio_detailed(
  id: int,
  *,
  client: AuthenticatedClient | Client,
  remove_from_client: bool | Unset = True,
  blocklist: bool | Unset = False,
  skip_redownload: bool | Unset = False,
  change_category: bool | Unset = False,
) -> Response[Any]:
  """
  Args:
      id (int):
      remove_from_client (bool | Unset):  Default: True.
      blocklist (bool | Unset):  Default: False.
      skip_redownload (bool | Unset):  Default: False.
      change_category (bool | Unset):  Default: False.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    id=id,
    remove_from_client=remove_from_client,
    blocklist=blocklist,
    skip_redownload=skip_redownload,
    change_category=change_category,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)
