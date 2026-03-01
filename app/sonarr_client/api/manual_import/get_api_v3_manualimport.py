from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.manual_import_resource import ManualImportResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  folder: str | Unset = UNSET,
  download_id: str | Unset = UNSET,
  series_id: int | Unset = UNSET,
  season_number: int | Unset = UNSET,
  filter_existing_files: bool | Unset = True,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["folder"] = folder

  params["downloadId"] = download_id

  params["seriesId"] = series_id

  params["seasonNumber"] = season_number

  params["filterExistingFiles"] = filter_existing_files

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/manualimport",
    "params": params,
  }

  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[ManualImportResource] | None:
  if response.status_code == 200:
    response_200 = []
    _response_200 = response.json()
    for response_200_item_data in _response_200:
      response_200_item = ManualImportResource.from_dict(response_200_item_data)

      response_200.append(response_200_item)

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[ManualImportResource]]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  folder: str | Unset = UNSET,
  download_id: str | Unset = UNSET,
  series_id: int | Unset = UNSET,
  season_number: int | Unset = UNSET,
  filter_existing_files: bool | Unset = True,
) -> Response[list[ManualImportResource]]:
  """
  Args:
      folder (str | Unset):
      download_id (str | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      filter_existing_files (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[ManualImportResource]]
  """

  kwargs = _get_kwargs(
    folder=folder,
    download_id=download_id,
    series_id=series_id,
    season_number=season_number,
    filter_existing_files=filter_existing_files,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  folder: str | Unset = UNSET,
  download_id: str | Unset = UNSET,
  series_id: int | Unset = UNSET,
  season_number: int | Unset = UNSET,
  filter_existing_files: bool | Unset = True,
) -> list[ManualImportResource] | None:
  """
  Args:
      folder (str | Unset):
      download_id (str | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      filter_existing_files (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[ManualImportResource]
  """

  return sync_detailed(
    client=client,
    folder=folder,
    download_id=download_id,
    series_id=series_id,
    season_number=season_number,
    filter_existing_files=filter_existing_files,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  folder: str | Unset = UNSET,
  download_id: str | Unset = UNSET,
  series_id: int | Unset = UNSET,
  season_number: int | Unset = UNSET,
  filter_existing_files: bool | Unset = True,
) -> Response[list[ManualImportResource]]:
  """
  Args:
      folder (str | Unset):
      download_id (str | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      filter_existing_files (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[list[ManualImportResource]]
  """

  kwargs = _get_kwargs(
    folder=folder,
    download_id=download_id,
    series_id=series_id,
    season_number=season_number,
    filter_existing_files=filter_existing_files,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  folder: str | Unset = UNSET,
  download_id: str | Unset = UNSET,
  series_id: int | Unset = UNSET,
  season_number: int | Unset = UNSET,
  filter_existing_files: bool | Unset = True,
) -> list[ManualImportResource] | None:
  """
  Args:
      folder (str | Unset):
      download_id (str | Unset):
      series_id (int | Unset):
      season_number (int | Unset):
      filter_existing_files (bool | Unset):  Default: True.

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      list[ManualImportResource]
  """

  return (
    await asyncio_detailed(
      client=client,
      folder=folder,
      download_id=download_id,
      series_id=series_id,
      season_number=season_number,
      filter_existing_files=filter_existing_files,
    )
  ).parsed
