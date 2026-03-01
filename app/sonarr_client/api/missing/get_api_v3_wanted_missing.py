from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.episode_resource_paging_resource import EpisodeResourcePagingResource
from ...models.sort_direction import SortDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_series: bool | Unset = False,
  include_images: bool | Unset = False,
  monitored: bool | Unset = True,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["page"] = page

  params["pageSize"] = page_size

  params["sortKey"] = sort_key

  json_sort_direction: str | Unset = UNSET
  if not isinstance(sort_direction, Unset):
    json_sort_direction = sort_direction.value

  params["sortDirection"] = json_sort_direction

  params["includeSeries"] = include_series

  params["includeImages"] = include_images

  params["monitored"] = monitored

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/wanted/missing",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EpisodeResourcePagingResource | None:
  if response.status_code == 200:
    response_200 = EpisodeResourcePagingResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[EpisodeResourcePagingResource]:
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
  include_series: bool | Unset = False,
  include_images: bool | Unset = False,
  monitored: bool | Unset = True,
) -> Response[EpisodeResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_series (bool | Unset):  Default: False.
      include_images (bool | Unset):  Default: False.
      monitored (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[EpisodeResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_series=include_series,
    include_images=include_images,
    monitored=monitored,
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
  include_series: bool | Unset = False,
  include_images: bool | Unset = False,
  monitored: bool | Unset = True,
) -> EpisodeResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_series (bool | Unset):  Default: False.
      include_images (bool | Unset):  Default: False.
      monitored (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      EpisodeResourcePagingResource
  """

  return sync_detailed(
    client=client,
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_series=include_series,
    include_images=include_images,
    monitored=monitored,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_series: bool | Unset = False,
  include_images: bool | Unset = False,
  monitored: bool | Unset = True,
) -> Response[EpisodeResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_series (bool | Unset):  Default: False.
      include_images (bool | Unset):  Default: False.
      monitored (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[EpisodeResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_series=include_series,
    include_images=include_images,
    monitored=monitored,
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
  include_series: bool | Unset = False,
  include_images: bool | Unset = False,
  monitored: bool | Unset = True,
) -> EpisodeResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_series (bool | Unset):  Default: False.
      include_images (bool | Unset):  Default: False.
      monitored (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      EpisodeResourcePagingResource
  """

  return (
    await asyncio_detailed(
      client=client,
      page=page,
      page_size=page_size,
      sort_key=sort_key,
      sort_direction=sort_direction,
      include_series=include_series,
      include_images=include_images,
      monitored=monitored,
    )
  ).parsed
