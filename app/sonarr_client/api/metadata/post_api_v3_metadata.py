from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metadata_resource import MetadataResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  body: MetadataResource | Unset = UNSET,
  force_save: bool | Unset = False,
) -> dict[str, Any]:
  headers: dict[str, Any] = {}

  params: dict[str, Any] = {}

  params["forceSave"] = force_save

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "post",
    "url": "/api/v3/metadata",
    "params": params,
  }

  if not isinstance(body, Unset):
    _kwargs["json"] = body.to_dict()

  headers["Content-Type"] = "application/json"

  _kwargs["headers"] = headers
  return _kwargs


def _parse_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MetadataResource | None:
  if response.status_code == 200:
    response_200 = MetadataResource.from_dict(response.json())

    return response_200

  if client.raise_on_unexpected_status:
    raise errors.UnexpectedStatus(response.status_code, response.content)
  else:
    return None


def _build_response(
  *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MetadataResource]:
  return Response(
    status_code=HTTPStatus(response.status_code),
    content=response.content,
    headers=response.headers,
    parsed=_parse_response(client=client, response=response),
  )


def sync_detailed(
  *,
  client: AuthenticatedClient | Client,
  body: MetadataResource | Unset = UNSET,
  force_save: bool | Unset = False,
) -> Response[MetadataResource]:
  """
  Args:
      force_save (bool | Unset):  Default: False.
      body (MetadataResource | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MetadataResource]
  """

  kwargs = _get_kwargs(
    body=body,
    force_save=force_save,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


def sync(
  *,
  client: AuthenticatedClient | Client,
  body: MetadataResource | Unset = UNSET,
  force_save: bool | Unset = False,
) -> MetadataResource | None:
  """
  Args:
      force_save (bool | Unset):  Default: False.
      body (MetadataResource | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MetadataResource
  """

  return sync_detailed(
    client=client,
    body=body,
    force_save=force_save,
  ).parsed


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  body: MetadataResource | Unset = UNSET,
  force_save: bool | Unset = False,
) -> Response[MetadataResource]:
  """
  Args:
      force_save (bool | Unset):  Default: False.
      body (MetadataResource | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[MetadataResource]
  """

  kwargs = _get_kwargs(
    body=body,
    force_save=force_save,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)


async def asyncio(
  *,
  client: AuthenticatedClient | Client,
  body: MetadataResource | Unset = UNSET,
  force_save: bool | Unset = False,
) -> MetadataResource | None:
  """
  Args:
      force_save (bool | Unset):  Default: False.
      body (MetadataResource | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      MetadataResource
  """

  return (
    await asyncio_detailed(
      client=client,
      body=body,
      force_save=force_save,
    )
  ).parsed
