from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.colon_replacement_format import ColonReplacementFormat
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  rename_movies: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: ColonReplacementFormat | Unset = UNSET,
  standard_movie_format: str | Unset = UNSET,
  movie_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["renameMovies"] = rename_movies

  params["replaceIllegalCharacters"] = replace_illegal_characters

  json_colon_replacement_format: str | Unset = UNSET
  if not isinstance(colon_replacement_format, Unset):
    json_colon_replacement_format = colon_replacement_format.value

  params["colonReplacementFormat"] = json_colon_replacement_format

  params["standardMovieFormat"] = standard_movie_format

  params["movieFolderFormat"] = movie_folder_format

  params["id"] = id

  params["resourceName"] = resource_name

  params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

  _kwargs: dict[str, Any] = {
    "method": "get",
    "url": "/api/v3/config/naming/examples",
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
  *,
  client: AuthenticatedClient | Client,
  rename_movies: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: ColonReplacementFormat | Unset = UNSET,
  standard_movie_format: str | Unset = UNSET,
  movie_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> Response[Any]:
  """
  Args:
      rename_movies (bool | Unset):
      replace_illegal_characters (bool | Unset):
      colon_replacement_format (ColonReplacementFormat | Unset):
      standard_movie_format (str | Unset):
      movie_folder_format (str | Unset):
      id (int | Unset):
      resource_name (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    rename_movies=rename_movies,
    replace_illegal_characters=replace_illegal_characters,
    colon_replacement_format=colon_replacement_format,
    standard_movie_format=standard_movie_format,
    movie_folder_format=movie_folder_format,
    id=id,
    resource_name=resource_name,
  )

  response = client.get_httpx_client().request(
    **kwargs,
  )

  return _build_response(client=client, response=response)


async def asyncio_detailed(
  *,
  client: AuthenticatedClient | Client,
  rename_movies: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: ColonReplacementFormat | Unset = UNSET,
  standard_movie_format: str | Unset = UNSET,
  movie_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> Response[Any]:
  """
  Args:
      rename_movies (bool | Unset):
      replace_illegal_characters (bool | Unset):
      colon_replacement_format (ColonReplacementFormat | Unset):
      standard_movie_format (str | Unset):
      movie_folder_format (str | Unset):
      id (int | Unset):
      resource_name (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    rename_movies=rename_movies,
    replace_illegal_characters=replace_illegal_characters,
    colon_replacement_format=colon_replacement_format,
    standard_movie_format=standard_movie_format,
    movie_folder_format=movie_folder_format,
    id=id,
    resource_name=resource_name,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)
