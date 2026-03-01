"""Contains all the data models used in inputs/outputs"""

from .add_movie_method import AddMovieMethod
from .add_movie_options import AddMovieOptions
from .alternative_title_resource import AlternativeTitleResource
from .api_info_resource import ApiInfoResource
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
from .calendar_release_type import CalendarReleaseType
from .certificate_validation_type import CertificateValidationType
from .collection_movie_resource import CollectionMovieResource
from .collection_resource import CollectionResource
from .collection_update_resource import CollectionUpdateResource
from .colon_replacement_format import ColonReplacementFormat
from .command import Command
from .command_priority import CommandPriority
from .command_resource import CommandResource
from .command_result import CommandResult
from .command_status import CommandStatus
from .command_trigger import CommandTrigger
from .credit_resource import CreditResource
from .credit_type import CreditType
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
from .extra_file_resource import ExtraFileResource
from .extra_file_type import ExtraFileType
from .field import Field
from .file_date_type import FileDateType
from .health_check_result import HealthCheckResult
from .health_resource import HealthResource
from .history_resource import HistoryResource
from .history_resource_data_type_0 import HistoryResourceDataType0
from .history_resource_paging_resource import HistoryResourcePagingResource
from .host_config_resource import HostConfigResource
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
from .language_resource import LanguageResource
from .localization_language_resource import LocalizationLanguageResource
from .log_file_resource import LogFileResource
from .log_resource import LogResource
from .log_resource_paging_resource import LogResourcePagingResource
from .manual_import_reprocess_resource import ManualImportReprocessResource
from .manual_import_resource import ManualImportResource
from .media_cover import MediaCover
from .media_cover_types import MediaCoverTypes
from .media_info_resource import MediaInfoResource
from .media_management_config_resource import MediaManagementConfigResource
from .metadata_config_resource import MetadataConfigResource
from .metadata_resource import MetadataResource
from .modifier import Modifier
from .monitor_types import MonitorTypes
from .movie_collection_resource import MovieCollectionResource
from .movie_editor_resource import MovieEditorResource
from .movie_file_list_resource import MovieFileListResource
from .movie_file_resource import MovieFileResource
from .movie_history_event_type import MovieHistoryEventType
from .movie_resource import MovieResource
from .movie_resource_paging_resource import MovieResourcePagingResource
from .movie_runtime_format_type import MovieRuntimeFormatType
from .movie_statistics_resource import MovieStatisticsResource
from .movie_status_type import MovieStatusType
from .naming_config_resource import NamingConfigResource
from .notification_resource import NotificationResource
from .parse_resource import ParseResource
from .parsed_movie_info import ParsedMovieInfo
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
from .rating_child import RatingChild
from .rating_type import RatingType
from .ratings import Ratings
from .rejection_type import RejectionType
from .release_profile_resource import ReleaseProfileResource
from .release_resource import ReleaseResource
from .remote_path_mapping_resource import RemotePathMappingResource
from .rename_movie_resource import RenameMovieResource
from .rescan_after_refresh_type import RescanAfterRefreshType
from .revision import Revision
from .root_folder_resource import RootFolderResource
from .runtime_mode import RuntimeMode
from .select_option import SelectOption
from .sort_direction import SortDirection
from .source_type import SourceType
from .system_resource import SystemResource
from .tag_details_resource import TagDetailsResource
from .tag_resource import TagResource
from .task_resource import TaskResource
from .tm_db_country_code import TMDbCountryCode
from .tracked_download_state import TrackedDownloadState
from .tracked_download_status import TrackedDownloadStatus
from .tracked_download_status_message import TrackedDownloadStatusMessage
from .ui_config_resource import UiConfigResource
from .unmapped_folder import UnmappedFolder
from .update_changes import UpdateChanges
from .update_mechanism import UpdateMechanism
from .update_resource import UpdateResource

__all__ = (
  "AddMovieMethod",
  "AddMovieOptions",
  "AlternativeTitleResource",
  "ApiInfoResource",
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
  "CalendarReleaseType",
  "CertificateValidationType",
  "CollectionMovieResource",
  "CollectionResource",
  "CollectionUpdateResource",
  "ColonReplacementFormat",
  "Command",
  "CommandPriority",
  "CommandResource",
  "CommandResult",
  "CommandStatus",
  "CommandTrigger",
  "CreditResource",
  "CreditType",
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
  "ExtraFileResource",
  "ExtraFileType",
  "Field",
  "FileDateType",
  "HealthCheckResult",
  "HealthResource",
  "HistoryResource",
  "HistoryResourceDataType0",
  "HistoryResourcePagingResource",
  "HostConfigResource",
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
  "LanguageResource",
  "LocalizationLanguageResource",
  "LogFileResource",
  "LogResource",
  "LogResourcePagingResource",
  "ManualImportReprocessResource",
  "ManualImportResource",
  "MediaCover",
  "MediaCoverTypes",
  "MediaInfoResource",
  "MediaManagementConfigResource",
  "MetadataConfigResource",
  "MetadataResource",
  "Modifier",
  "MonitorTypes",
  "MovieCollectionResource",
  "MovieEditorResource",
  "MovieFileListResource",
  "MovieFileResource",
  "MovieHistoryEventType",
  "MovieResource",
  "MovieResourcePagingResource",
  "MovieRuntimeFormatType",
  "MovieStatisticsResource",
  "MovieStatusType",
  "NamingConfigResource",
  "NotificationResource",
  "ParsedMovieInfo",
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
  "RatingChild",
  "Ratings",
  "RatingType",
  "RejectionType",
  "ReleaseProfileResource",
  "ReleaseResource",
  "RemotePathMappingResource",
  "RenameMovieResource",
  "RescanAfterRefreshType",
  "Revision",
  "RootFolderResource",
  "RuntimeMode",
  "SelectOption",
  "SortDirection",
  "SourceType",
  "SystemResource",
  "TagDetailsResource",
  "TagResource",
  "TaskResource",
  "TMDbCountryCode",
  "TrackedDownloadState",
  "TrackedDownloadStatus",
  "TrackedDownloadStatusMessage",
  "UiConfigResource",
  "UnmappedFolder",
  "UpdateChanges",
  "UpdateMechanism",
  "UpdateResource",
)
