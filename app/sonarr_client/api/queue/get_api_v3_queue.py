from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.download_protocol import DownloadProtocol
from ...models.queue_resource_paging_resource import QueueResourcePagingResource
from ...models.queue_status import QueueStatus
from ...models.sort_direction import SortDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_unknown_series_items: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
  series_ids: list[int] | Unset = UNSET,
  protocol: DownloadProtocol | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
  status: list[QueueStatus] | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["page"] = page

  params["pageSize"] = page_size

  params["sortKey"] = sort_key

  json_sort_direction: str | Unset = UNSET
  if not isinstance(sort_direction, Unset):
    json_sort_direction = sort_direction.value

  params["sortDirection"] = json_sort_direction

  params["includeUnknownSeriesItems"] = include_unknown_series_items

  params["includeSeries"] = include_series

  params["includeEpisode"] = include_episode

  json_series_ids: list[int] | Unset = UNSET
  if not isinstance(series_ids, Unset):
    json_series_ids = series_ids

  params["seriesIds"] = json_series_ids

  json_protocol: str | Unset = UNSET
  if not isinstance(protocol, Unset):
    json_protocol = protocol.value

  params["protocol"] = json_protocol

  json_languages: list[int] | Unset = UNSET
  if not isinstance(languages, Unset):
    json_languages = languages

  params["languages"] = json_languages

  json_quality: list[int] | Unset = UNSET
  if not isinstance(quality, Unset):
    json_quality = quality

  params["quality"] = json_quality

  json_status: list[str] | Unset = UNSET
  if not isinstance(status, Unset):
    json_status = []
    for status_item_data in status:
      status_item = status_item_data.value
      json_status.append(status_item)

  params["status"] = json_status

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/queue",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> QueueResourcePagingResource | None:
  if response.status_code == 200:
    response_200 = QueueResourcePagingResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[QueueResourcePagingResource]:
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
  include_unknown_series_items: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
  series_ids: list[int] | Unset = UNSET,
  protocol: DownloadProtocol | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
  status: list[QueueStatus] | Unset = UNSET,
) -> Response[QueueResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_unknown_series_items (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.
      series_ids (list[int] | Unset):
      protocol (DownloadProtocol | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):
      status (list[QueueStatus] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[QueueResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_unknown_series_items=include_unknown_series_items,
    include_series=include_series,
    include_episode=include_episode,
    series_ids=series_ids,
    protocol=protocol,
    languages=languages,
    quality=quality,
    status=status,
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
  include_unknown_series_items: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
  series_ids: list[int] | Unset = UNSET,
  protocol: DownloadProtocol | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
  status: list[QueueStatus] | Unset = UNSET,
) -> QueueResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_unknown_series_items (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.
      series_ids (list[int] | Unset):
      protocol (DownloadProtocol | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):
      status (list[QueueStatus] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      QueueResourcePagingResource
  """

  return sync_detailed(
    client=client,
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_unknown_series_items=include_unknown_series_items,
    include_series=include_series,
    include_episode=include_episode,
    series_ids=series_ids,
    protocol=protocol,
    languages=languages,
    quality=quality,
    status=status,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_unknown_series_items: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
  series_ids: list[int] | Unset = UNSET,
  protocol: DownloadProtocol | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
  status: list[QueueStatus] | Unset = UNSET,
) -> Response[QueueResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_unknown_series_items (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.
      series_ids (list[int] | Unset):
      protocol (DownloadProtocol | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):
      status (list[QueueStatus] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[QueueResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_unknown_series_items=include_unknown_series_items,
    include_series=include_series,
    include_episode=include_episode,
    series_ids=series_ids,
    protocol=protocol,
    languages=languages,
    quality=quality,
    status=status,
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
  include_unknown_series_items: bool | Unset = False,
  include_series: bool | Unset = False,
  include_episode: bool | Unset = False,
  series_ids: list[int] | Unset = UNSET,
  protocol: DownloadProtocol | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
  status: list[QueueStatus] | Unset = UNSET,
) -> QueueResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_unknown_series_items (bool | Unset):  Default: False.
      include_series (bool | Unset):  Default: False.
      include_episode (bool | Unset):  Default: False.
      series_ids (list[int] | Unset):
      protocol (DownloadProtocol | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):
      status (list[QueueStatus] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      QueueResourcePagingResource
  """

  return (
    await asyncio_detailed(
      client=client,
      page=page,
      page_size=page_size,
      sort_key=sort_key,
      sort_direction=sort_direction,
      include_unknown_series_items=include_unknown_series_items,
      include_series=include_series,
      include_episode=include_episode,
      series_ids=series_ids,
      protocol=protocol,
      languages=languages,
      quality=quality,
      status=status,
    )
  ).parsed
