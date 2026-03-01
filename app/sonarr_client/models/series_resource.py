from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.new_item_monitor_types import NewItemMonitorTypes
from ..models.series_status_type import SeriesStatusType
from ..models.series_types import SeriesTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.add_series_options import AddSeriesOptions
  from ..models.alternate_title_resource import AlternateTitleResource
  from ..models.language import Language
  from ..models.media_cover import MediaCover
  from ..models.ratings import Ratings
  from ..models.season_resource import SeasonResource
  from ..models.series_statistics_resource import SeriesStatisticsResource


T = TypeVar("T", bound="SeriesResource")


@_attrs_define
class SeriesResource:
  """
  Attributes:
      id (int | Unset):
      title (None | str | Unset):
      alternate_titles (list[AlternateTitleResource] | None | Unset):
      sort_title (None | str | Unset):
      status (SeriesStatusType | Unset):
      ended (bool | Unset):
      profile_name (None | str | Unset):
      overview (None | str | Unset):
      next_airing (datetime.datetime | None | Unset):
      previous_airing (datetime.datetime | None | Unset):
      network (None | str | Unset):
      air_time (None | str | Unset):
      images (list[MediaCover] | None | Unset):
      original_language (Language | Unset):
      remote_poster (None | str | Unset):
      seasons (list[SeasonResource] | None | Unset):
      year (int | Unset):
      path (None | str | Unset):
      quality_profile_id (int | Unset):
      season_folder (bool | Unset):
      monitored (bool | Unset):
      monitor_new_items (NewItemMonitorTypes | Unset):
      use_scene_numbering (bool | Unset):
      runtime (int | Unset):
      tvdb_id (int | Unset):
      tv_rage_id (int | Unset):
      tv_maze_id (int | Unset):
      tmdb_id (int | Unset):
      first_aired (datetime.datetime | None | Unset):
      last_aired (datetime.datetime | None | Unset):
      series_type (SeriesTypes | Unset):
      clean_title (None | str | Unset):
      imdb_id (None | str | Unset):
      title_slug (None | str | Unset):
      root_folder_path (None | str | Unset):
      folder (None | str | Unset):
      certification (None | str | Unset):
      genres (list[str] | None | Unset):
      tags (list[int] | None | Unset):
      added (datetime.datetime | Unset):
      add_options (AddSeriesOptions | Unset):
      ratings (Ratings | Unset):
      statistics (SeriesStatisticsResource | Unset):
      episodes_changed (bool | None | Unset):
      language_profile_id (int | Unset):
  """

  id: int | Unset = UNSET
  title: None | str | Unset = UNSET
  alternate_titles: list[AlternateTitleResource] | None | Unset = UNSET
  sort_title: None | str | Unset = UNSET
  status: SeriesStatusType | Unset = UNSET
  ended: bool | Unset = UNSET
  profile_name: None | str | Unset = UNSET
  overview: None | str | Unset = UNSET
  next_airing: datetime.datetime | None | Unset = UNSET
  previous_airing: datetime.datetime | None | Unset = UNSET
  network: None | str | Unset = UNSET
  air_time: None | str | Unset = UNSET
  images: list[MediaCover] | None | Unset = UNSET
  original_language: Language | Unset = UNSET
  remote_poster: None | str | Unset = UNSET
  seasons: list[SeasonResource] | None | Unset = UNSET
  year: int | Unset = UNSET
  path: None | str | Unset = UNSET
  quality_profile_id: int | Unset = UNSET
  season_folder: bool | Unset = UNSET
  monitored: bool | Unset = UNSET
  monitor_new_items: NewItemMonitorTypes | Unset = UNSET
  use_scene_numbering: bool | Unset = UNSET
  runtime: int | Unset = UNSET
  tvdb_id: int | Unset = UNSET
  tv_rage_id: int | Unset = UNSET
  tv_maze_id: int | Unset = UNSET
  tmdb_id: int | Unset = UNSET
  first_aired: datetime.datetime | None | Unset = UNSET
  last_aired: datetime.datetime | None | Unset = UNSET
  series_type: SeriesTypes | Unset = UNSET
  clean_title: None | str | Unset = UNSET
  imdb_id: None | str | Unset = UNSET
  title_slug: None | str | Unset = UNSET
  root_folder_path: None | str | Unset = UNSET
  folder: None | str | Unset = UNSET
  certification: None | str | Unset = UNSET
  genres: list[str] | None | Unset = UNSET
  tags: list[int] | None | Unset = UNSET
  added: datetime.datetime | Unset = UNSET
  add_options: AddSeriesOptions | Unset = UNSET
  ratings: Ratings | Unset = UNSET
  statistics: SeriesStatisticsResource | Unset = UNSET
  episodes_changed: bool | None | Unset = UNSET
  language_profile_id: int | Unset = UNSET

  def to_dict(self) -> dict[str, Any]:
    id = self.id

    title: None | str | Unset
    if isinstance(self.title, Unset):
      title = UNSET
    else:
      title = self.title

    alternate_titles: list[dict[str, Any]] | None | Unset
    if isinstance(self.alternate_titles, Unset):
      alternate_titles = UNSET
    elif isinstance(self.alternate_titles, list):
      alternate_titles = []
      for alternate_titles_type_0_item_data in self.alternate_titles:
        alternate_titles_type_0_item = alternate_titles_type_0_item_data.to_dict()
        alternate_titles.append(alternate_titles_type_0_item)

    else:
      alternate_titles = self.alternate_titles

    sort_title: None | str | Unset
    if isinstance(self.sort_title, Unset):
      sort_title = UNSET
    else:
      sort_title = self.sort_title

    status: str | Unset = UNSET
    if not isinstance(self.status, Unset):
      status = self.status.value

    ended = self.ended

    profile_name: None | str | Unset
    if isinstance(self.profile_name, Unset):
      profile_name = UNSET
    else:
      profile_name = self.profile_name

    overview: None | str | Unset
    if isinstance(self.overview, Unset):
      overview = UNSET
    else:
      overview = self.overview

    next_airing: None | str | Unset
    if isinstance(self.next_airing, Unset):
      next_airing = UNSET
    elif isinstance(self.next_airing, datetime.datetime):
      next_airing = self.next_airing.isoformat()
    else:
      next_airing = self.next_airing

    previous_airing: None | str | Unset
    if isinstance(self.previous_airing, Unset):
      previous_airing = UNSET
    elif isinstance(self.previous_airing, datetime.datetime):
      previous_airing = self.previous_airing.isoformat()
    else:
      previous_airing = self.previous_airing

    network: None | str | Unset
    if isinstance(self.network, Unset):
      network = UNSET
    else:
      network = self.network

    air_time: None | str | Unset
    if isinstance(self.air_time, Unset):
      air_time = UNSET
    else:
      air_time = self.air_time

    images: list[dict[str, Any]] | None | Unset
    if isinstance(self.images, Unset):
      images = UNSET
    elif isinstance(self.images, list):
      images = []
      for images_type_0_item_data in self.images:
        images_type_0_item = images_type_0_item_data.to_dict()
        images.append(images_type_0_item)

    else:
      images = self.images

    original_language: dict[str, Any] | Unset = UNSET
    if not isinstance(self.original_language, Unset):
      original_language = self.original_language.to_dict()

    remote_poster: None | str | Unset
    if isinstance(self.remote_poster, Unset):
      remote_poster = UNSET
    else:
      remote_poster = self.remote_poster

    seasons: list[dict[str, Any]] | None | Unset
    if isinstance(self.seasons, Unset):
      seasons = UNSET
    elif isinstance(self.seasons, list):
      seasons = []
      for seasons_type_0_item_data in self.seasons:
        seasons_type_0_item = seasons_type_0_item_data.to_dict()
        seasons.append(seasons_type_0_item)

    else:
      seasons = self.seasons

    year = self.year

    path: None | str | Unset
    if isinstance(self.path, Unset):
      path = UNSET
    else:
      path = self.path

    quality_profile_id = self.quality_profile_id

    season_folder = self.season_folder

    monitored = self.monitored

    monitor_new_items: str | Unset = UNSET
    if not isinstance(self.monitor_new_items, Unset):
      monitor_new_items = self.monitor_new_items.value

    use_scene_numbering = self.use_scene_numbering

    runtime = self.runtime

    tvdb_id = self.tvdb_id

    tv_rage_id = self.tv_rage_id

    tv_maze_id = self.tv_maze_id

    tmdb_id = self.tmdb_id

    first_aired: None | str | Unset
    if isinstance(self.first_aired, Unset):
      first_aired = UNSET
    elif isinstance(self.first_aired, datetime.datetime):
      first_aired = self.first_aired.isoformat()
    else:
      first_aired = self.first_aired

    last_aired: None | str | Unset
    if isinstance(self.last_aired, Unset):
      last_aired = UNSET
    elif isinstance(self.last_aired, datetime.datetime):
      last_aired = self.last_aired.isoformat()
    else:
      last_aired = self.last_aired

    series_type: str | Unset = UNSET
    if not isinstance(self.series_type, Unset):
      series_type = self.series_type.value

    clean_title: None | str | Unset
    if isinstance(self.clean_title, Unset):
      clean_title = UNSET
    else:
      clean_title = self.clean_title

    imdb_id: None | str | Unset
    if isinstance(self.imdb_id, Unset):
      imdb_id = UNSET
    else:
      imdb_id = self.imdb_id

    title_slug: None | str | Unset
    if isinstance(self.title_slug, Unset):
      title_slug = UNSET
    else:
      title_slug = self.title_slug

    root_folder_path: None | str | Unset
    if isinstance(self.root_folder_path, Unset):
      root_folder_path = UNSET
    else:
      root_folder_path = self.root_folder_path

    folder: None | str | Unset
    if isinstance(self.folder, Unset):
      folder = UNSET
    else:
      folder = self.folder

    certification: None | str | Unset
    if isinstance(self.certification, Unset):
      certification = UNSET
    else:
      certification = self.certification

    genres: list[str] | None | Unset
    if isinstance(self.genres, Unset):
      genres = UNSET
    elif isinstance(self.genres, list):
      genres = self.genres

    else:
      genres = self.genres

    tags: list[int] | None | Unset
    if isinstance(self.tags, Unset):
      tags = UNSET
    elif isinstance(self.tags, list):
      tags = self.tags

    else:
      tags = self.tags

    added: str | Unset = UNSET
    if not isinstance(self.added, Unset):
      added = self.added.isoformat()

    add_options: dict[str, Any] | Unset = UNSET
    if not isinstance(self.add_options, Unset):
      add_options = self.add_options.to_dict()

    ratings: dict[str, Any] | Unset = UNSET
    if not isinstance(self.ratings, Unset):
      ratings = self.ratings.to_dict()

    statistics: dict[str, Any] | Unset = UNSET
    if not isinstance(self.statistics, Unset):
      statistics = self.statistics.to_dict()

    episodes_changed: bool | None | Unset
    if isinstance(self.episodes_changed, Unset):
      episodes_changed = UNSET
    else:
      episodes_changed = self.episodes_changed

    language_profile_id = self.language_profile_id

    field_dict: dict[str, Any] = {}

    field_dict.update({})
    if id is not UNSET:
      field_dict["id"] = id
    if title is not UNSET:
      field_dict["title"] = title
    if alternate_titles is not UNSET:
      field_dict["alternateTitles"] = alternate_titles
    if sort_title is not UNSET:
      field_dict["sortTitle"] = sort_title
    if status is not UNSET:
      field_dict["status"] = status
    if ended is not UNSET:
      field_dict["ended"] = ended
    if profile_name is not UNSET:
      field_dict["profileName"] = profile_name
    if overview is not UNSET:
      field_dict["overview"] = overview
    if next_airing is not UNSET:
      field_dict["nextAiring"] = next_airing
    if previous_airing is not UNSET:
      field_dict["previousAiring"] = previous_airing
    if network is not UNSET:
      field_dict["network"] = network
    if air_time is not UNSET:
      field_dict["airTime"] = air_time
    if images is not UNSET:
      field_dict["images"] = images
    if original_language is not UNSET:
      field_dict["originalLanguage"] = original_language
    if remote_poster is not UNSET:
      field_dict["remotePoster"] = remote_poster
    if seasons is not UNSET:
      field_dict["seasons"] = seasons
    if year is not UNSET:
      field_dict["year"] = year
    if path is not UNSET:
      field_dict["path"] = path
    if quality_profile_id is not UNSET:
      field_dict["qualityProfileId"] = quality_profile_id
    if season_folder is not UNSET:
      field_dict["seasonFolder"] = season_folder
    if monitored is not UNSET:
      field_dict["monitored"] = monitored
    if monitor_new_items is not UNSET:
      field_dict["monitorNewItems"] = monitor_new_items
    if use_scene_numbering is not UNSET:
      field_dict["useSceneNumbering"] = use_scene_numbering
    if runtime is not UNSET:
      field_dict["runtime"] = runtime
    if tvdb_id is not UNSET:
      field_dict["tvdbId"] = tvdb_id
    if tv_rage_id is not UNSET:
      field_dict["tvRageId"] = tv_rage_id
    if tv_maze_id is not UNSET:
      field_dict["tvMazeId"] = tv_maze_id
    if tmdb_id is not UNSET:
      field_dict["tmdbId"] = tmdb_id
    if first_aired is not UNSET:
      field_dict["firstAired"] = first_aired
    if last_aired is not UNSET:
      field_dict["lastAired"] = last_aired
    if series_type is not UNSET:
      field_dict["seriesType"] = series_type
    if clean_title is not UNSET:
      field_dict["cleanTitle"] = clean_title
    if imdb_id is not UNSET:
      field_dict["imdbId"] = imdb_id
    if title_slug is not UNSET:
      field_dict["titleSlug"] = title_slug
    if root_folder_path is not UNSET:
      field_dict["rootFolderPath"] = root_folder_path
    if folder is not UNSET:
      field_dict["folder"] = folder
    if certification is not UNSET:
      field_dict["certification"] = certification
    if genres is not UNSET:
      field_dict["genres"] = genres
    if tags is not UNSET:
      field_dict["tags"] = tags
    if added is not UNSET:
      field_dict["added"] = added
    if add_options is not UNSET:
      field_dict["addOptions"] = add_options
    if ratings is not UNSET:
      field_dict["ratings"] = ratings
    if statistics is not UNSET:
      field_dict["statistics"] = statistics
    if episodes_changed is not UNSET:
      field_dict["episodesChanged"] = episodes_changed
    if language_profile_id is not UNSET:
      field_dict["languageProfileId"] = language_profile_id

    return field_dict

  @classmethod
  def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
    from ..models.add_series_options import AddSeriesOptions
    from ..models.alternate_title_resource import AlternateTitleResource
    from ..models.language import Language
    from ..models.media_cover import MediaCover
    from ..models.ratings import Ratings
    from ..models.season_resource import SeasonResource
    from ..models.series_statistics_resource import SeriesStatisticsResource

    d = dict(src_dict)
    id = d.pop("id", UNSET)

    def _parse_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title = _parse_title(d.pop("title", UNSET))

    def _parse_alternate_titles(data: object) -> list[AlternateTitleResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        alternate_titles_type_0 = []
        _alternate_titles_type_0 = data
        for alternate_titles_type_0_item_data in _alternate_titles_type_0:
          alternate_titles_type_0_item = AlternateTitleResource.from_dict(
            alternate_titles_type_0_item_data
          )

          alternate_titles_type_0.append(alternate_titles_type_0_item)

        return alternate_titles_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[AlternateTitleResource] | None | Unset, data)

    alternate_titles = _parse_alternate_titles(d.pop("alternateTitles", UNSET))

    def _parse_sort_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    sort_title = _parse_sort_title(d.pop("sortTitle", UNSET))

    _status = d.pop("status", UNSET)
    status: SeriesStatusType | Unset
    if isinstance(_status, Unset):
      status = UNSET
    else:
      status = SeriesStatusType(_status)

    ended = d.pop("ended", UNSET)

    def _parse_profile_name(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    profile_name = _parse_profile_name(d.pop("profileName", UNSET))

    def _parse_overview(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    overview = _parse_overview(d.pop("overview", UNSET))

    def _parse_next_airing(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        next_airing_type_0 = isoparse(data)

        return next_airing_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    next_airing = _parse_next_airing(d.pop("nextAiring", UNSET))

    def _parse_previous_airing(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        previous_airing_type_0 = isoparse(data)

        return previous_airing_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    previous_airing = _parse_previous_airing(d.pop("previousAiring", UNSET))

    def _parse_network(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    network = _parse_network(d.pop("network", UNSET))

    def _parse_air_time(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    air_time = _parse_air_time(d.pop("airTime", UNSET))

    def _parse_images(data: object) -> list[MediaCover] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        images_type_0 = []
        _images_type_0 = data
        for images_type_0_item_data in _images_type_0:
          images_type_0_item = MediaCover.from_dict(images_type_0_item_data)

          images_type_0.append(images_type_0_item)

        return images_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[MediaCover] | None | Unset, data)

    images = _parse_images(d.pop("images", UNSET))

    _original_language = d.pop("originalLanguage", UNSET)
    original_language: Language | Unset
    if isinstance(_original_language, Unset):
      original_language = UNSET
    else:
      original_language = Language.from_dict(_original_language)

    def _parse_remote_poster(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    remote_poster = _parse_remote_poster(d.pop("remotePoster", UNSET))

    def _parse_seasons(data: object) -> list[SeasonResource] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        seasons_type_0 = []
        _seasons_type_0 = data
        for seasons_type_0_item_data in _seasons_type_0:
          seasons_type_0_item = SeasonResource.from_dict(seasons_type_0_item_data)

          seasons_type_0.append(seasons_type_0_item)

        return seasons_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[SeasonResource] | None | Unset, data)

    seasons = _parse_seasons(d.pop("seasons", UNSET))

    year = d.pop("year", UNSET)

    def _parse_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    path = _parse_path(d.pop("path", UNSET))

    quality_profile_id = d.pop("qualityProfileId", UNSET)

    season_folder = d.pop("seasonFolder", UNSET)

    monitored = d.pop("monitored", UNSET)

    _monitor_new_items = d.pop("monitorNewItems", UNSET)
    monitor_new_items: NewItemMonitorTypes | Unset
    if isinstance(_monitor_new_items, Unset):
      monitor_new_items = UNSET
    else:
      monitor_new_items = NewItemMonitorTypes(_monitor_new_items)

    use_scene_numbering = d.pop("useSceneNumbering", UNSET)

    runtime = d.pop("runtime", UNSET)

    tvdb_id = d.pop("tvdbId", UNSET)

    tv_rage_id = d.pop("tvRageId", UNSET)

    tv_maze_id = d.pop("tvMazeId", UNSET)

    tmdb_id = d.pop("tmdbId", UNSET)

    def _parse_first_aired(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        first_aired_type_0 = isoparse(data)

        return first_aired_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    first_aired = _parse_first_aired(d.pop("firstAired", UNSET))

    def _parse_last_aired(data: object) -> datetime.datetime | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, str):
          raise TypeError()
        last_aired_type_0 = isoparse(data)

        return last_aired_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(datetime.datetime | None | Unset, data)

    last_aired = _parse_last_aired(d.pop("lastAired", UNSET))

    _series_type = d.pop("seriesType", UNSET)
    series_type: SeriesTypes | Unset
    if isinstance(_series_type, Unset):
      series_type = UNSET
    else:
      series_type = SeriesTypes(_series_type)

    def _parse_clean_title(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    clean_title = _parse_clean_title(d.pop("cleanTitle", UNSET))

    def _parse_imdb_id(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    imdb_id = _parse_imdb_id(d.pop("imdbId", UNSET))

    def _parse_title_slug(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    title_slug = _parse_title_slug(d.pop("titleSlug", UNSET))

    def _parse_root_folder_path(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    root_folder_path = _parse_root_folder_path(d.pop("rootFolderPath", UNSET))

    def _parse_folder(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    folder = _parse_folder(d.pop("folder", UNSET))

    def _parse_certification(data: object) -> None | str | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(None | str | Unset, data)

    certification = _parse_certification(d.pop("certification", UNSET))

    def _parse_genres(data: object) -> list[str] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        genres_type_0 = cast(list[str], data)

        return genres_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[str] | None | Unset, data)

    genres = _parse_genres(d.pop("genres", UNSET))

    def _parse_tags(data: object) -> list[int] | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      try:
        if not isinstance(data, list):
          raise TypeError()
        tags_type_0 = cast(list[int], data)

        return tags_type_0
      except TypeError, ValueError, AttributeError, KeyError:
        pass
      return cast(list[int] | None | Unset, data)

    tags = _parse_tags(d.pop("tags", UNSET))

    _added = d.pop("added", UNSET)
    added: datetime.datetime | Unset
    if isinstance(_added, Unset):
      added = UNSET
    else:
      added = isoparse(_added)

    _add_options = d.pop("addOptions", UNSET)
    add_options: AddSeriesOptions | Unset
    if isinstance(_add_options, Unset):
      add_options = UNSET
    else:
      add_options = AddSeriesOptions.from_dict(_add_options)

    _ratings = d.pop("ratings", UNSET)
    ratings: Ratings | Unset
    if isinstance(_ratings, Unset):
      ratings = UNSET
    else:
      ratings = Ratings.from_dict(_ratings)

    _statistics = d.pop("statistics", UNSET)
    statistics: SeriesStatisticsResource | Unset
    if isinstance(_statistics, Unset):
      statistics = UNSET
    else:
      statistics = SeriesStatisticsResource.from_dict(_statistics)

    def _parse_episodes_changed(data: object) -> bool | None | Unset:
      if data is None:
        return data
      if isinstance(data, Unset):
        return data
      return cast(bool | None | Unset, data)

    episodes_changed = _parse_episodes_changed(d.pop("episodesChanged", UNSET))

    language_profile_id = d.pop("languageProfileId", UNSET)

    series_resource = cls(
      id=id,
      title=title,
      alternate_titles=alternate_titles,
      sort_title=sort_title,
      status=status,
      ended=ended,
      profile_name=profile_name,
      overview=overview,
      next_airing=next_airing,
      previous_airing=previous_airing,
      network=network,
      air_time=air_time,
      images=images,
      original_language=original_language,
      remote_poster=remote_poster,
      seasons=seasons,
      year=year,
      path=path,
      quality_profile_id=quality_profile_id,
      season_folder=season_folder,
      monitored=monitored,
      monitor_new_items=monitor_new_items,
      use_scene_numbering=use_scene_numbering,
      runtime=runtime,
      tvdb_id=tvdb_id,
      tv_rage_id=tv_rage_id,
      tv_maze_id=tv_maze_id,
      tmdb_id=tmdb_id,
      first_aired=first_aired,
      last_aired=last_aired,
      series_type=series_type,
      clean_title=clean_title,
      imdb_id=imdb_id,
      title_slug=title_slug,
      root_folder_path=root_folder_path,
      folder=folder,
      certification=certification,
      genres=genres,
      tags=tags,
      added=added,
      add_options=add_options,
      ratings=ratings,
      statistics=statistics,
      episodes_changed=episodes_changed,
      language_profile_id=language_profile_id,
    )

    return series_resource
