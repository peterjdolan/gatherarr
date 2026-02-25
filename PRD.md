# PRD: Gatherarr (Minimal Arr Search Worker)

## Purpose

Gatherarr is a small, worker-style daemon that periodically triggers search-related operations in
supported `*arr` services. It is intended for self-hosted users who want predictable automation
with low operational complexity.

## Functional Requirements

- Load all runtime settings from environment variables at startup.
- Validate config and fail fast with clear errors for missing/invalid values.
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

## State Management Requirements

- Keep state minimal:
  - per target: last run timestamp, last success timestamp, last status, consecutive failures,
    last error summary.
  - per target item: item identifier, last processed timestamp, last result/status.
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
- Never log API keys or full auth headers.
- Graceful shutdown should finish in-flight work or stop within timeout.
- Container runtime must run as non-root.

## Testing and Quality Requirements

- Unit tests:
  - config parsing and validation,
  - scheduler timing logic,
  - retry/backoff behavior,
  - state serialization and atomic write behavior,
  - metrics emission helpers.
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
