from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.history_resource_paging_resource import HistoryResourcePagingResource
from ...models.sort_direction import SortDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_movie: bool | Unset = UNSET,
  event_type: list[int] | Unset = UNSET,
  download_id: str | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["page"] = page

  params["pageSize"] = page_size

  params["sortKey"] = sort_key

  json_sort_direction: str | Unset = UNSET
  if not isinstance(sort_direction, Unset):
    json_sort_direction = sort_direction.value

  params["sortDirection"] = json_sort_direction

  params["includeMovie"] = include_movie

  json_event_type: list[int] | Unset = UNSET
  if not isinstance(event_type, Unset):
    json_event_type = event_type

  params["eventType"] = json_event_type

  params["downloadId"] = download_id

  json_movie_ids: list[int] | Unset = UNSET
  if not isinstance(movie_ids, Unset):
    json_movie_ids = movie_ids

  params["movieIds"] = json_movie_ids

  json_languages: list[int] | Unset = UNSET
  if not isinstance(languages, Unset):
    json_languages = languages

  params["languages"] = json_languages

  json_quality: list[int] | Unset = UNSET
  if not isinstance(quality, Unset):
    json_quality = quality

  params["quality"] = json_quality

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/history",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HistoryResourcePagingResource | None:
  if response.status_code == 200:
    response_200 = HistoryResourcePagingResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HistoryResourcePagingResource]:
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
  include_movie: bool | Unset = UNSET,
  event_type: list[int] | Unset = UNSET,
  download_id: str | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
) -> Response[HistoryResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_movie (bool | Unset):
      event_type (list[int] | Unset):
      download_id (str | Unset):
      movie_ids (list[int] | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[HistoryResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_movie=include_movie,
    event_type=event_type,
    download_id=download_id,
    movie_ids=movie_ids,
    languages=languages,
    quality=quality,
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
  include_movie: bool | Unset = UNSET,
  event_type: list[int] | Unset = UNSET,
  download_id: str | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
) -> HistoryResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_movie (bool | Unset):
      event_type (list[int] | Unset):
      download_id (str | Unset):
      movie_ids (list[int] | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      HistoryResourcePagingResource
  """

  return sync_detailed(
    client=client,
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_movie=include_movie,
    event_type=event_type,
    download_id=download_id,
    movie_ids=movie_ids,
    languages=languages,
    quality=quality,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  page: int | Unset = 1,
  page_size: int | Unset = 10,
  sort_key: str | Unset = UNSET,
  sort_direction: SortDirection | Unset = UNSET,
  include_movie: bool | Unset = UNSET,
  event_type: list[int] | Unset = UNSET,
  download_id: str | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
) -> Response[HistoryResourcePagingResource]:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_movie (bool | Unset):
      event_type (list[int] | Unset):
      download_id (str | Unset):
      movie_ids (list[int] | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[HistoryResourcePagingResource]
  """

  kwargs = _get_kwargs(
    page=page,
    page_size=page_size,
    sort_key=sort_key,
    sort_direction=sort_direction,
    include_movie=include_movie,
    event_type=event_type,
    download_id=download_id,
    movie_ids=movie_ids,
    languages=languages,
    quality=quality,
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
  include_movie: bool | Unset = UNSET,
  event_type: list[int] | Unset = UNSET,
  download_id: str | Unset = UNSET,
  movie_ids: list[int] | Unset = UNSET,
  languages: list[int] | Unset = UNSET,
  quality: list[int] | Unset = UNSET,
) -> HistoryResourcePagingResource | None:
  """
  Args:
      page (int | Unset):  Default: 1.
      page_size (int | Unset):  Default: 10.
      sort_key (str | Unset):
      sort_direction (SortDirection | Unset):
      include_movie (bool | Unset):
      event_type (list[int] | Unset):
      download_id (str | Unset):
      movie_ids (list[int] | Unset):
      languages (list[int] | Unset):
      quality (list[int] | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      HistoryResourcePagingResource
  """

  return (
    await asyncio_detailed(
      client=client,
      page=page,
      page_size=page_size,
      sort_key=sort_key,
      sort_direction=sort_direction,
      include_movie=include_movie,
      event_type=event_type,
      download_id=download_id,
      movie_ids=movie_ids,
      languages=languages,
      quality=quality,
    )
  ).parsed
