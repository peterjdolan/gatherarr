# PRD: Gatherarr (Minimal Arr Search Worker)

## Purpose

Gatherarr is a small, worker-style daemon that periodically triggers search-related operations in
supported `*arr` services. It is intended for self-hosted users who want predictable automation
with low operational complexity.

### Compatibility Policy

Gatherarr does not offer backwards-compatibility guarantees for configuration until v1.0. Configuration variable names, formats, and behavior may change between releases without migration support. Users should expect to update their configuration when upgrading.

## Functional Requirements

- Load all runtime settings from environment variables at startup.
- Validate config and fail fast with clear errors for missing/invalid values. On validation failure, output a concise summary of all detected issues (missing vars, invalid values, duplicate target names).
- Reject duplicate target names (`GTH_ARR_<n>_NAME`); each target must have a unique name.
- Reject startup if any unrecognized environment variables starting with `GTH_` are present (e.g. typos like `GTH_ARR_0_TYPO` or obsolete vars).
- For each configured target instance:
  - authenticate via API key,
  - issue supported search action(s),
  - record attempt outcome and timestamps.
- Supported search scope is:
  - Movies (Radarr)
  - Individual seasons (Sonarr)
- Explicitly out of scope:
  - Series-wide searches
  - Episode-level searches
- Execute runs at configured intervals with per-target and global operation limits.
- Handle transient API failures using configurable HTTP retry with exponential backoff.
- When an item search fails, apply configurable failed-search retry backoff before reattempting.
- Persist state after each run or attempt outcome.
- Recover previous state on restart.
- Expose Prometheus metrics endpoint (`/metrics`).
- Emit structured logs to stdout/stderr.
- Apply configurable search eligibility filters to determine which items should be searched.

## Search Eligibility Requirements

Gatherarr supports configurable filtering criteria to determine which items are eligible for search operations. All eligibility criteria can be configured globally with per-target overrides.

### Eligibility Criteria

- **Monitored Status** (`require_monitored`, default: `true`):
  - For Radarr: Only search movies that are monitored.
  - For Sonarr: Only search seasons where both the season and series are monitored (when series monitoring status is available).

- **Quality Cutoff** (`require_cutoff_unmet`, default: `true`):
  - For Radarr: Only search movies that have not met their quality cutoff (either no file present, or `qualityCutoffNotMet` is true).
  - For Sonarr: Only search seasons where episode file count is less than total episode count, or quality cutoff has not been met.

- **Release Status** (`released_only`, default: `false`):
  - For Radarr: Only search movies that have been released (have a file, or any release date - digital, physical, or cinema - has passed).
  - For Sonarr: Only search seasons that have released episodes (episode file count > 0, or previous airing date has passed, or series first aired date has passed).

- **Tag Filtering** (`include_tags`, `exclude_tags`, default: empty):
  - `include_tags`: Comma-separated list of tags. Items must have at least one matching tag to be eligible.
  - `exclude_tags`: Comma-separated list of tags. Items with any matching tag are excluded.
  - For Radarr: Uses movie tags.
  - For Sonarr: Uses series tags.

- **Missing Episode Thresholds** (Sonarr only, default: `0`):
  - `min_missing_episodes`: Minimum number of missing episodes required for a season to be eligible.
  - `min_missing_percent`: Minimum percentage of missing episodes required (0.0-100.0).
  - Both thresholds must be satisfied if both are set to non-zero values.

### Search Backoff (Failed-Search Retry)

See **Retry Configuration** for full failed-search retry parameters. Items with previous error status are subject to the configured retry backoff before being eligible again.

### Revisit Behavior

- Items that were successfully searched are subject to `item_revisit_s` before being eligible again.
- Items that failed are subject to the failed-search retry backoff (see Retry Configuration) before being eligible again.
- Revisit timeout and search backoff are independent and both must be satisfied.

### Dry Run Mode

- **Dry Run** (`dry_run`, default: `false`):
  - When enabled, eligibility checks are performed and items are marked as eligible in state, but no actual search API calls are made.
  - Useful for testing eligibility criteria without triggering searches.

## Retry Configuration

Gatherarr supports configurable retry behavior for two scenarios: transient HTTP failures and failed item searches. All parameters support global defaults with per-target overrides.

### HTTP Retries

Applied when an HTTP request to a *arr API fails with a retryable error (network error, `5xx`, `429`):

- **HTTP max retries** (`http_max_retries`): Maximum number of retry attempts per request. Default: `3`.
- **HTTP initial retry delay** (`http_retry_initial_delay_s`): Delay in seconds before the first retry. Default: `1.0`.
- **HTTP retry backoff exponent** (`http_retry_backoff_exponent`): Multiplier for exponential backoff (e.g. `2.0` means delay doubles each attempt). Default: `2.0`.
- **HTTP retry max delay** (`http_retry_max_delay_s`): Cap on delay between retries in seconds. Default: `30.0`.

### Failed-Search Retries

Applied when an item's search fails; determines how long to wait before retrying that item on a subsequent run:

- **Search max retries** (`search_retry_max_attempts`): Maximum retry attempts for a failed item (`0` = retry indefinitely). Default: `5`.
- **Search initial retry delay** (`search_retry_initial_delay_s`): Initial delay in seconds before first retry. Default: `60`.
- **Search retry backoff exponent** (`search_retry_backoff_exponent`): Multiplier for exponential backoff. Default: `2.0`.
- **Search retry max delay** (`search_retry_max_delay_s`): Cap on delay between retries in seconds. Default: `86400` (24 hours).

## State Management Requirements

- State is persisted to a single YAML file. No other state storage format is supported.
- Keep state minimal:
  - per target: last run timestamp, last success timestamp, last status, consecutive failures,
    last error summary.
  - per target item: item identifier, last processed timestamp, last result/status (SUCCESS, ERROR, or UNKNOWN).
  - global: process start timestamp, total runs.
- State size is capped at 10 MB. When the state file would exceed this limit, prune the oldest item state entries (oldest `last_processed_timestamp` first) until the size is within the cap. This ensures bounded storage and predictable behavior.
- Use atomic write semantics:
  1. write to temp file in the same directory,
  2. fsync temp file,
  3. atomic rename/replace to target path,
  4. optionally fsync parent directory where supported.
- On corrupted state file:
  - log parsing error,
  - move file aside as `.corrupt.<timestamp>`,
  - continue with fresh state.

## Observability Requirements

### Startup Banner

- At startup, after configuration is loaded and validated, emit a startup banner to logs.
- The banner MUST display an easily readable copy of the full configuration (global settings and per-target settings).
- Purpose: allow users to quickly verify their per-target configuration is as expected before the first run.
- Omit sensitive values (API keys) from the banner; redact or omit entirely.

### Metrics (minimum)

- `gatherarr_run_total{target,type,status}` counter
- `gatherarr_requests_total{target,type}` counter
- `gatherarr_grabs_total{target,type}` counter
- `gatherarr_skips_total{target,type}` counter
- `gatherarr_request_errors_total{target,type}` counter
- `gatherarr_request_duration_seconds{target,type}` histogram (distribution of individual request durations)
- `gatherarr_last_success_timestamp_seconds{target,type}` gauge
- `gatherarr_state_write_failures_total` counter

### Logging

- ALL INFO level logs MUST be structured JSON output to stdout/stderr.
- ALL INFO level logs MUST indicate and ONLY indicate actions taken that materially affects a target.
- Include correlation fields: `target_name`, `target_type`, `run_id`.
- For item-related actions, include:
  - Movies: `movie_id` field
  - Seasons: `series_id` and `season_number` fields

## Reliability and Security Requirements

- Apply configurable timeouts for all external HTTP calls (`http_timeout_s`, default: `30`).
- Retry only retryable failures (`network`, `5xx`, `429`) using configurable HTTP retry (see Retry Configuration).
- Use a logging redaction layer to mask sensitive parameters in all structured log output (API keys, `Authorization`, `Cookie`, bearer tokens, and similar).
- Never log API keys or full auth headers.
- `/metrics` is served without built-in authentication; deployments that need auth MUST enforce it via external auth controls and/or network access restrictions.
- If a target `base_url` uses plain HTTP, API keys are transmitted in cleartext over the network; use HTTPS wherever possible.
- Graceful shutdown should finish in-flight work or stop within a configurable timeout (`shutdown_timeout_s`, default: `30`).
- Container runtime must run as non-root.

## Testing and Quality Requirements

- Unit tests:
  - config parsing and validation (including duplicate target names),
  - scheduler timing logic,
  - HTTP retry/backoff behavior,
  - failed-search retry/backoff behavior,
  - state serialization, atomic write behavior, and size-cap pruning,
  - metrics emission helpers,
  - search eligibility filtering logic (monitored status, cutoff unmet, release status, tag filtering, missing episode thresholds),
  - search backoff and revisit timeout behavior.
- Integration tests:
  - fake Radarr/Sonarr interaction scenarios (success, `4xx`, `5xx`, timeout),
  - state recovery from previous file,
  - `/metrics` scrape assertions.
- E2E/container smoke tests:
  - `docker run` with env vars and mounted state volume,
  - verify run cycle, state updates, and metrics endpoint response.
- Quality gates:
  - CI checks for lint, type-check, and tests,
  - high coverage target (for example, >=`85%`) with focus on scheduler/state/retry paths.

## Deployment Requirements

- Build and publish a single Docker image.
- Read configuration only from environment variables.
- Require persistent mount for the state file path. The state file is YAML format.
- Expose a health endpoint (`/health`) that returns `"OK"` only when:
  - liveness is satisfied (process is running), and
  - readiness is satisfied (configuration is valid and scheduler is initialized).
- The health endpoint MUST always be available and served, regardless of whether the metrics endpoint is enabled. When metrics are disabled, a minimal HTTP server still runs to serve `/health`.
- The health and metrics endpoints MUST be bound to the same listen address and port. Configuration uses general parameters (`listen_address`, `listen_port`) rather than metrics-specific names, since the HTTP server hosts both endpoints.

## Milestones

### v0.1 (Current)

**Scope:** Radarr and Sonarr only.

**Planned features and changes:**

- **Retry configuration**
  - HTTP retries: configurable `http_max_retries`, `http_retry_initial_delay_s`, `http_retry_backoff_exponent`, `http_retry_max_delay_s` (global and per-target).
  - Failed-search retries: configurable `search_retry_max_attempts`, `search_retry_initial_delay_s`, `search_retry_backoff_exponent`, `search_retry_max_delay_s` (global and per-target).
- **HTTP timeout:** Configurable `http_timeout_s` for all external HTTP calls.
- **Graceful shutdown:** Configurable `shutdown_timeout_s`; finish in-flight work or stop within timeout.
- **Startup banner:** Emit an easily readable copy of the full configuration (global and per-target) at startup so users can verify per-target configuration. Exclude API keys.
- **Health always live:** Serve `/health` even when metrics are disabled; run a minimal HTTP server for health regardless of `GTH_METRICS_ENABLED`. Rename `metrics_address`/`metrics_port` to `listen_address`/`listen_port` (`GTH_LISTEN_ADDRESS`, `GTH_LISTEN_PORT`) to reflect that the server hosts both health and metrics endpoints.
- **Config validation:** On startup failure, output a concise summary of all validation issues (missing vars, invalid values). Reject duplicate target names.
- **Log redaction:** Expand sensitive-key redaction to cover `Authorization`, `Cookie`, bearer tokens, and similar.
- **State size cap:** Cap state file at 10 MB; prune oldest item state entries when the limit would be exceeded.

**Architectural changes (readability, robustness, testability, security):**

- **Scheduler module split:** Extract `MovieHandler` and `SeasonHandler` from the scheduler into dedicated handler modules (`app/handlers/`) to reduce file size and improve readability.
- **ItemHandler protocol documentation:** Document the ItemHandler contract (extract_item_id, extract_logging_id, should_search, search) in the PRD to support consistent Fake implementations and future extensibility (e.g. Lidarr in v0.2).
- **HTTP base URL validation:** At config load, warn or fail when a target `base_url` uses `http://` instead of `https://`, since API keys are transmitted in cleartext over HTTP.
- **Configuration schema documentation:** Document the full environment variable schema (names, types, defaults, per-target overrides) in README or a dedicated config reference so the source of truth is explicit and testable.

### v0.2 (Future)

**Scope:** Additional *arr apps.

- Lidarr support.
- Whisparr support.
- Any app-specific eligibility logic for new apps.
