"""Contains all the data models used in inputs/outputs"""

from .add_series_options import AddSeriesOptions
from .alternate_title_resource import AlternateTitleResource
from .apply_tags import ApplyTags
from .authentication_required_type import AuthenticationRequiredType
from .authentication_type import AuthenticationType
from .auto_tagging_resource import AutoTaggingResource
from .auto_tagging_specification_schema import AutoTaggingSpecificationSchema
from .backup_resource import BackupResource
from .backup_type import BackupType
from .blocklist_bulk_resource import BlocklistBulkResource
from .blocklist_resource import BlocklistResource
from .blocklist_resource_paging_resource import BlocklistResourcePagingResource
from .certificate_validation_type import CertificateValidationType
from .command import Command
from .command_priority import CommandPriority
from .command_resource import CommandResource
from .command_result import CommandResult
from .command_status import CommandStatus
from .command_trigger import CommandTrigger
from .custom_filter_resource import CustomFilterResource
from .custom_filter_resource_filters_type_0_item import CustomFilterResourceFiltersType0Item
from .custom_format_bulk_resource import CustomFormatBulkResource
from .custom_format_resource import CustomFormatResource
from .custom_format_specification_schema import CustomFormatSpecificationSchema
from .database_type import DatabaseType
from .delay_profile_resource import DelayProfileResource
from .disk_space_resource import DiskSpaceResource
from .download_client_bulk_resource import DownloadClientBulkResource
from .download_client_config_resource import DownloadClientConfigResource
from .download_client_resource import DownloadClientResource
from .download_protocol import DownloadProtocol
from .episode_file_list_resource import EpisodeFileListResource
from .episode_file_resource import EpisodeFileResource
from .episode_history_event_type import EpisodeHistoryEventType
from .episode_resource import EpisodeResource
from .episode_resource_paging_resource import EpisodeResourcePagingResource
from .episode_title_required_type import EpisodeTitleRequiredType
from .episodes_monitored_resource import EpisodesMonitoredResource
from .field import Field
from .file_date_type import FileDateType
from .health_check_result import HealthCheckResult
from .health_resource import HealthResource
from .history_resource import HistoryResource
from .history_resource_data_type_0 import HistoryResourceDataType0
from .history_resource_paging_resource import HistoryResourcePagingResource
from .host_config_resource import HostConfigResource
from .http_uri import HttpUri
from .import_list_bulk_resource import ImportListBulkResource
from .import_list_config_resource import ImportListConfigResource
from .import_list_exclusion_bulk_resource import ImportListExclusionBulkResource
from .import_list_exclusion_resource import ImportListExclusionResource
from .import_list_exclusion_resource_paging_resource import (
  ImportListExclusionResourcePagingResource,
)
from .import_list_resource import ImportListResource
from .import_list_type import ImportListType
from .import_rejection_resource import ImportRejectionResource
from .indexer_bulk_resource import IndexerBulkResource
from .indexer_config_resource import IndexerConfigResource
from .indexer_flag_resource import IndexerFlagResource
from .indexer_resource import IndexerResource
from .language import Language
from .language_profile_item_resource import LanguageProfileItemResource
from .language_profile_resource import LanguageProfileResource
from .language_resource import LanguageResource
from .list_sync_level_type import ListSyncLevelType
from .localization_language_resource import LocalizationLanguageResource
from .localization_resource import LocalizationResource
from .localization_resource_strings_type_0 import LocalizationResourceStringsType0
from .log_file_resource import LogFileResource
from .log_resource import LogResource
from .log_resource_paging_resource import LogResourcePagingResource
from .manual_import_reprocess_resource import ManualImportReprocessResource
from .manual_import_resource import ManualImportResource
from .media_cover import MediaCover
from .media_cover_types import MediaCoverTypes
from .media_info_resource import MediaInfoResource
from .media_management_config_resource import MediaManagementConfigResource
from .metadata_resource import MetadataResource
from .monitor_types import MonitorTypes
from .monitoring_options import MonitoringOptions
from .naming_config_resource import NamingConfigResource
from .new_item_monitor_types import NewItemMonitorTypes
from .notification_resource import NotificationResource
from .parse_resource import ParseResource
from .parsed_episode_info import ParsedEpisodeInfo
from .ping_resource import PingResource
from .post_login_body import PostLoginBody
from .privacy_level import PrivacyLevel
from .profile_format_item_resource import ProfileFormatItemResource
from .proper_download_types import ProperDownloadTypes
from .provider_message import ProviderMessage
from .provider_message_type import ProviderMessageType
from .proxy_type import ProxyType
from .quality import Quality
from .quality_definition_limits_resource import QualityDefinitionLimitsResource
from .quality_definition_resource import QualityDefinitionResource
from .quality_model import QualityModel
from .quality_profile_quality_item_resource import QualityProfileQualityItemResource
from .quality_profile_resource import QualityProfileResource
from .quality_source import QualitySource
from .queue_bulk_resource import QueueBulkResource
from .queue_resource import QueueResource
from .queue_resource_paging_resource import QueueResourcePagingResource
from .queue_status import QueueStatus
from .queue_status_resource import QueueStatusResource
from .ratings import Ratings
from .rejection_type import RejectionType
from .release_episode_resource import ReleaseEpisodeResource
from .release_profile_resource import ReleaseProfileResource
from .release_resource import ReleaseResource
from .release_type import ReleaseType
from .remote_path_mapping_resource import RemotePathMappingResource
from .rename_episode_resource import RenameEpisodeResource
from .rescan_after_refresh_type import RescanAfterRefreshType
from .revision import Revision
from .root_folder_resource import RootFolderResource
from .runtime_mode import RuntimeMode
from .season_pass_resource import SeasonPassResource
from .season_pass_series_resource import SeasonPassSeriesResource
from .season_resource import SeasonResource
from .season_statistics_resource import SeasonStatisticsResource
from .select_option import SelectOption
from .series_editor_resource import SeriesEditorResource
from .series_resource import SeriesResource
from .series_statistics_resource import SeriesStatisticsResource
from .series_status_type import SeriesStatusType
from .series_title_info import SeriesTitleInfo
from .series_types import SeriesTypes
from .sort_direction import SortDirection
from .system_resource import SystemResource
from .tag_details_resource import TagDetailsResource
from .tag_resource import TagResource
from .task_resource import TaskResource
from .tracked_download_state import TrackedDownloadState
from .tracked_download_status import TrackedDownloadStatus
from .tracked_download_status_message import TrackedDownloadStatusMessage
from .ui_config_resource import UiConfigResource
from .unmapped_folder import UnmappedFolder
from .update_changes import UpdateChanges
from .update_mechanism import UpdateMechanism
from .update_resource import UpdateResource

__all__ = (
  "AddSeriesOptions",
  "AlternateTitleResource",
  "ApplyTags",
  "AuthenticationRequiredType",
  "AuthenticationType",
  "AutoTaggingResource",
  "AutoTaggingSpecificationSchema",
  "BackupResource",
  "BackupType",
  "BlocklistBulkResource",
  "BlocklistResource",
  "BlocklistResourcePagingResource",
  "CertificateValidationType",
  "Command",
  "CommandPriority",
  "CommandResource",
  "CommandResult",
  "CommandStatus",
  "CommandTrigger",
  "CustomFilterResource",
  "CustomFilterResourceFiltersType0Item",
  "CustomFormatBulkResource",
  "CustomFormatResource",
  "CustomFormatSpecificationSchema",
  "DatabaseType",
  "DelayProfileResource",
  "DiskSpaceResource",
  "DownloadClientBulkResource",
  "DownloadClientConfigResource",
  "DownloadClientResource",
  "DownloadProtocol",
  "EpisodeFileListResource",
  "EpisodeFileResource",
  "EpisodeHistoryEventType",
  "EpisodeResource",
  "EpisodeResourcePagingResource",
  "EpisodesMonitoredResource",
  "EpisodeTitleRequiredType",
  "Field",
  "FileDateType",
  "HealthCheckResult",
  "HealthResource",
  "HistoryResource",
  "HistoryResourceDataType0",
  "HistoryResourcePagingResource",
  "HostConfigResource",
  "HttpUri",
  "ImportListBulkResource",
  "ImportListConfigResource",
  "ImportListExclusionBulkResource",
  "ImportListExclusionResource",
  "ImportListExclusionResourcePagingResource",
  "ImportListResource",
  "ImportListType",
  "ImportRejectionResource",
  "IndexerBulkResource",
  "IndexerConfigResource",
  "IndexerFlagResource",
  "IndexerResource",
  "Language",
  "LanguageProfileItemResource",
  "LanguageProfileResource",
  "LanguageResource",
  "ListSyncLevelType",
  "LocalizationLanguageResource",
  "LocalizationResource",
  "LocalizationResourceStringsType0",
  "LogFileResource",
  "LogResource",
  "LogResourcePagingResource",
  "ManualImportReprocessResource",
  "ManualImportResource",
  "MediaCover",
  "MediaCoverTypes",
  "MediaInfoResource",
  "MediaManagementConfigResource",
  "MetadataResource",
  "MonitoringOptions",
  "MonitorTypes",
  "NamingConfigResource",
  "NewItemMonitorTypes",
  "NotificationResource",
  "ParsedEpisodeInfo",
  "ParseResource",
  "PingResource",
  "PostLoginBody",
  "PrivacyLevel",
  "ProfileFormatItemResource",
  "ProperDownloadTypes",
  "ProviderMessage",
  "ProviderMessageType",
  "ProxyType",
  "Quality",
  "QualityDefinitionLimitsResource",
  "QualityDefinitionResource",
  "QualityModel",
  "QualityProfileQualityItemResource",
  "QualityProfileResource",
  "QualitySource",
  "QueueBulkResource",
  "QueueResource",
  "QueueResourcePagingResource",
  "QueueStatus",
  "QueueStatusResource",
  "Ratings",
  "RejectionType",
  "ReleaseEpisodeResource",
  "ReleaseProfileResource",
  "ReleaseResource",
  "ReleaseType",
  "RemotePathMappingResource",
  "RenameEpisodeResource",
  "RescanAfterRefreshType",
  "Revision",
  "RootFolderResource",
  "RuntimeMode",
  "SeasonPassResource",
  "SeasonPassSeriesResource",
  "SeasonResource",
  "SeasonStatisticsResource",
  "SelectOption",
  "SeriesEditorResource",
  "SeriesResource",
  "SeriesStatisticsResource",
  "SeriesStatusType",
  "SeriesTitleInfo",
  "SeriesTypes",
  "SortDirection",
  "SystemResource",
  "TagDetailsResource",
  "TagResource",
  "TaskResource",
  "TrackedDownloadState",
  "TrackedDownloadStatus",
  "TrackedDownloadStatusMessage",
  "UiConfigResource",
  "UnmappedFolder",
  "UpdateChanges",
  "UpdateMechanism",
  "UpdateResource",
)
