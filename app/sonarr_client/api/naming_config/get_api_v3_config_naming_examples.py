from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
  *,
  rename_episodes: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: int | Unset = UNSET,
  custom_colon_replacement_format: str | Unset = UNSET,
  multi_episode_style: int | Unset = UNSET,
  standard_episode_format: str | Unset = UNSET,
  daily_episode_format: str | Unset = UNSET,
  anime_episode_format: str | Unset = UNSET,
  series_folder_format: str | Unset = UNSET,
  season_folder_format: str | Unset = UNSET,
  specials_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> dict[str, Any]:

  params: dict[str, Any] = {}

  params["renameEpisodes"] = rename_episodes

  params["replaceIllegalCharacters"] = replace_illegal_characters

  params["colonReplacementFormat"] = colon_replacement_format

  params["customColonReplacementFormat"] = custom_colon_replacement_format

  params["multiEpisodeStyle"] = multi_episode_style

  params["standardEpisodeFormat"] = standard_episode_format

  params["dailyEpisodeFormat"] = daily_episode_format

  params["animeEpisodeFormat"] = anime_episode_format

  params["seriesFolderFormat"] = series_folder_format

  params["seasonFolderFormat"] = season_folder_format

  params["specialsFolderFormat"] = specials_folder_format

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
  rename_episodes: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: int | Unset = UNSET,
  custom_colon_replacement_format: str | Unset = UNSET,
  multi_episode_style: int | Unset = UNSET,
  standard_episode_format: str | Unset = UNSET,
  daily_episode_format: str | Unset = UNSET,
  anime_episode_format: str | Unset = UNSET,
  series_folder_format: str | Unset = UNSET,
  season_folder_format: str | Unset = UNSET,
  specials_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> Response[Any]:
  """
  Args:
      rename_episodes (bool | Unset):
      replace_illegal_characters (bool | Unset):
      colon_replacement_format (int | Unset):
      custom_colon_replacement_format (str | Unset):
      multi_episode_style (int | Unset):
      standard_episode_format (str | Unset):
      daily_episode_format (str | Unset):
      anime_episode_format (str | Unset):
      series_folder_format (str | Unset):
      season_folder_format (str | Unset):
      specials_folder_format (str | Unset):
      id (int | Unset):
      resource_name (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    rename_episodes=rename_episodes,
    replace_illegal_characters=replace_illegal_characters,
    colon_replacement_format=colon_replacement_format,
    custom_colon_replacement_format=custom_colon_replacement_format,
    multi_episode_style=multi_episode_style,
    standard_episode_format=standard_episode_format,
    daily_episode_format=daily_episode_format,
    anime_episode_format=anime_episode_format,
    series_folder_format=series_folder_format,
    season_folder_format=season_folder_format,
    specials_folder_format=specials_folder_format,
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
  rename_episodes: bool | Unset = UNSET,
  replace_illegal_characters: bool | Unset = UNSET,
  colon_replacement_format: int | Unset = UNSET,
  custom_colon_replacement_format: str | Unset = UNSET,
  multi_episode_style: int | Unset = UNSET,
  standard_episode_format: str | Unset = UNSET,
  daily_episode_format: str | Unset = UNSET,
  anime_episode_format: str | Unset = UNSET,
  series_folder_format: str | Unset = UNSET,
  season_folder_format: str | Unset = UNSET,
  specials_folder_format: str | Unset = UNSET,
  id: int | Unset = UNSET,
  resource_name: str | Unset = UNSET,
) -> Response[Any]:
  """
  Args:
      rename_episodes (bool | Unset):
      replace_illegal_characters (bool | Unset):
      colon_replacement_format (int | Unset):
      custom_colon_replacement_format (str | Unset):
      multi_episode_style (int | Unset):
      standard_episode_format (str | Unset):
      daily_episode_format (str | Unset):
      anime_episode_format (str | Unset):
      series_folder_format (str | Unset):
      season_folder_format (str | Unset):
      specials_folder_format (str | Unset):
      id (int | Unset):
      resource_name (str | Unset):

  Raises:
      errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
      httpx.TimeoutException: If the request takes longer than Client.timeout.

  Returns:
      Response[Any]
  """

  kwargs = _get_kwargs(
    rename_episodes=rename_episodes,
    replace_illegal_characters=replace_illegal_characters,
    colon_replacement_format=colon_replacement_format,
    custom_colon_replacement_format=custom_colon_replacement_format,
    multi_episode_style=multi_episode_style,
    standard_episode_format=standard_episode_format,
    daily_episode_format=daily_episode_format,
    anime_episode_format=anime_episode_format,
    series_folder_format=series_folder_format,
    season_folder_format=season_folder_format,
    specials_folder_format=specials_folder_format,
    id=id,
    resource_name=resource_name,
  )

  response = await client.get_async_httpx_client().request(**kwargs)

  return _build_response(client=client, response=response)
