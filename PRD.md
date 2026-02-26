# PRD: Gatherarr (Minimal Arr Search Worker)

## Purpose

Gatherarr is a small, worker-style daemon that periodically triggers search-related operations in
supported `*arr` services. It is intended for self-hosted users who want predictable automation
with low operational complexity.

## Functional Requirements

- Load all runtime settings from environment variables at startup.
- Validate config and fail fast with clear errors for missing/invalid values.
- Reject startup if any unrecognized environment variables starting with `GTH_` are
  present (e.g. typos like `GTH_ARR_0_TYPO` or obsolete vars).
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
- Handle transient API failures using bounded retry/backoff.
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

### Search Backoff

- **Search Backoff** (`search_backoff_s`, default: `0`):
  - When an item search fails, wait at least this many seconds before attempting to search again.
  - Only applies to items with previous error status.
  - When set to `0`, no backoff is applied (failed items can be retried immediately if revisit timeout allows).

### Revisit Behavior

- Items that were successfully searched are subject to `item_revisit_s` before being eligible again.
- Items that failed are subject to `search_backoff_s` (if configured) before being eligible again.
- Revisit timeout and search backoff are independent and both must be satisfied.

### Dry Run Mode

- **Dry Run** (`dry_run`, default: `false`):
  - When enabled, eligibility checks are performed and items are marked as eligible in state, but no actual search API calls are made.
  - Useful for testing eligibility criteria without triggering searches.

## State Management Requirements

- Keep state minimal:
  - per target: last run timestamp, last success timestamp, last status, consecutive failures,
    last error summary.
  - per target item: item identifier, last processed timestamp, last result/status (SUCCESS, ERROR, or UNKNOWN).
  - global: process start timestamp, total runs.
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

- Apply explicit timeouts for all external HTTP calls.
- Retry only retryable failures (`network`, `5xx`, `429`).
- Use a logging redaction layer to mask API key parameters in all structured log output.
- Never log API keys or full auth headers.
- `/metrics` is served without built-in authentication; deployments that need auth MUST enforce it via external auth controls and/or network access restrictions.
- If a target `base_url` uses plain HTTP, API keys are transmitted in cleartext over the network; use HTTPS wherever possible.
- Graceful shutdown should finish in-flight work or stop within timeout.
- Container runtime must run as non-root.

## Testing and Quality Requirements

- Unit tests:
  - config parsing and validation,
  - scheduler timing logic,
  - retry/backoff behavior,
  - state serialization and atomic write behavior,
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
- Require persistent mount for state file path.
- Expose one health endpoint (`/health`) that returns `"OK"` only when:
  - liveness is satisfied (process is running), and
  - readiness is satisfied (configuration is valid and scheduler is initialized).
