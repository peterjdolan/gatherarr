from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blocklist_resource_paging_resource import BlocklistResourcePagingResource
from ...models.download_protocol import DownloadProtocol
from ...models.sort_direction import SortDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  protocols: list[DownloadProtocol] | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["page"] = page

  params["pageSize"] = page_size

  params["sortKey"] = sort_key

  json_sort_direction: str | Unset = UNSET
  if not isinstance(sort_direction, Unset):
    json_sort_direction = sort_direction.value

  params["sortDirection"] = json_sort_direction

  json_movie_ids: list[int] | Unset = UNSET
  if not isinstance(movie_ids, Unset):
    json_movie_ids = movie_ids

  params["movieIds"] = json_movie_ids

  json_protocols: list[str] | Unset = UNSET
  if not isinstance(protocols, Unset):
    json_protocols = []
    for protocols_item_data in protocols:
      protocols_item = protocols_item_data.value
      json_protocols.append(protocols_item)

  params["protocols"] = json_protocols

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/blocklist",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BlocklistResourcePagingResource | None:
  if response.status_code == 200:
    response_200 = BlocklistResourcePagingResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BlocklistResourcePagingResource]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  protocols: list[DownloadProtocol] | Unset = UNSET,
) -> Response[BlocklistResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      movie_ids (list[int] | Unset):
      protocols (list[DownloadProtocol] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[BlocklistResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    movie_ids=movie_ids,
    protocols=protocols,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  protocols: list[DownloadProtocol] | Unset = UNSET,
) -> BlocklistResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      movie_ids (list[int] | Unset):
      protocols (list[DownloadProtocol] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      BlocklistResourcePagingResource
  """

  return sync_detailed(
    client=client,
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    movie_ids=movie_ids,
    protocols=protocols,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  protocols: list[DownloadProtocol] | Unset = UNSET,
) -> Response[BlocklistResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      movie_ids (list[int] | Unset):
      protocols (list[DownloadProtocol] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[BlocklistResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    movie_ids=movie_ids,
    protocols=protocols,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  protocols: list[DownloadProtocol] | Unset = UNSET,
) -> BlocklistResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      movie_ids (list[int] | Unset):
      protocols (list[DownloadProtocol] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      BlocklistResourcePagingResource
  """

  return (
    await asyncio_detailed(
      client=client,
      page=page,
      page_size=page_size,
      sort_key=sort_key,
      sort_direction=sort_direction,
      movie_ids=movie_ids,
      protocols=protocols,
    )
  ).parsed
