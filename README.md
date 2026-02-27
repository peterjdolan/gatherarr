# Gatherarr

[![CI](https://img.shields.io/github/actions/workflow/status/peterjdolan/gatherarr/ci.yml?branch=main&label=CI)](https://github.com/peterjdolan/gatherarr/actions/workflows/ci.yml)
[![Docker Image](https://img.shields.io/github/actions/workflow/status/peterjdolan/gatherarr/docker-image.yml?branch=main&label=Docker%20Image)](https://github.com/peterjdolan/gatherarr/actions/workflows/docker-image.yml)
[![Docker Image Version](https://img.shields.io/docker/v/astrocatcmdr/gatherarr?sort=semver&logo=docker)](https://hub.docker.com/r/astrocatcmdr/gatherarr)
[![Docker Image Size](https://img.shields.io/docker/image-size/astrocatcmdr/gatherarr?logo=docker)](https://hub.docker.com/r/astrocatcmdr/gatherarr)
[![Docker Pulls](https://img.shields.io/docker/pulls/astrocatcmdr/gatherarr?logo=docker)](https://hub.docker.com/r/astrocatcmdr/gatherarr)
[![License](https://img.shields.io/github/license/peterjdolan/gatherarr)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)

A lightweight service that performs one job: periodically trigger searches in supported *arr apps.

Huntarrs are great, but when you need a calm, reliable, and simple helper, you need a Gatherarr.

- **Goal:** Simple, reliable, observable background searches for *arr apps.
- **Deployment model:** Docker container only.
- **Configuration model:** Environment variables only.
- **Security model:** No sensitive information written to disk or emitted in logs. No outgoing network requests except to the configured *arr servers. No telemetry or monitoring.

For full product requirements, architecture, and planned features, see [PRD.md](PRD.md).

## Roadmap

- **v0.1 (coming soon):** Retry configuration (HTTP and failed-search), configurable HTTP timeout and graceful shutdown, startup banner with full config display, health endpoint always served (independent of metrics), config validation summary, expanded log redaction, state size cap (10 MB), and architectural improvements (ItemHandler protocol, HTTP base URL validation).
- **v0.2:** Lidarr and Whisparr support.
- **v1.0:** Backwards compatibility for configuration. Until v1.0, configuration variable names and behavior may change between releases.

## Minimal Deployment with Docker Compose

```yaml
services:
  gatherarr:
    image: astrocatcmdr/gatherarr:latest
    container_name: gatherarr
    environment:
      GTH_ARR_0_TYPE: radarr
      GTH_ARR_0_NAME: Radarr
      GTH_ARR_0_BASEURL: http://radarr:7878
      GTH_ARR_0_APIKEY: FAKE_RADARR_API_KEY_REPLACE_ME
      GTH_ARR_1_TYPE: sonarr
      GTH_ARR_1_NAME: Sonarr
      GTH_ARR_1_BASEURL: http://sonarr:8989
      GTH_ARR_1_APIKEY: FAKE_SONARR_API_KEY_REPLACE_ME
```

For complex setups, use Docker `.env` files or Docker Secrets for API keys.

## Configuration

Configuration is done by environment variables only. Docker Compose users are welcome to use `.env` files for configuration management, and Docker Secrets to manage sensitive API tokens.

Gatherarr will not start if any unrecognized environment variables beginning with `GTH_` are present. This helps detect typos (e.g. `GTH_ARR_0_TYPO` instead of `GTH_ARR_0_TYPE`) and obsolete configuration.

### Global configuration

- `GTH_LOG_LEVEL`: (Optional) log verbosity, `debug|info|warn|error`, default `info`.
- `GTH_STATE_FILE_PATH`: (Optional) path to state persistence file, default `/data/state.yaml`.
- `GTH_METRICS_ENABLED`: (Optional) Whether or not to host the metrics endpoint, `true|false`, default `false`.
- `GTH_METRICS_ADDRESS`: (Optional) Metrics endpoint listen address, default `0.0.0.0`.
- `GTH_METRICS_PORT`: (Optional) Metrics endpoint port, default `9090`.
- `GTH_OPS_PER_INTERVAL`: (Optional) Common number of operations to perform per interval time, default `1`.
- `GTH_INTERVAL_S`: (Optional) Common interval duration in seconds, default `60`.
- `GTH_ITEM_REVISIT_S`: (Optional) Minimum time in seconds to wait before reprocessing a previously successfully processed item, default `604800` (one week).
- `GTH_REQUIRE_MONITORED`: (Optional) Only search monitored items, `true|false`, default `true`.
- `GTH_REQUIRE_CUTOFF_UNMET`: (Optional) Only search items that haven't met quality cutoff, `true|false`, default `true`.
- `GTH_RELEASED_ONLY`: (Optional) Only search items that have been released, `true|false`, default `false`.
- `GTH_SEARCH_BACKOFF_S`: (Optional) Minimum time in seconds to wait before retrying a previously failed item search, default `0` (no backoff).
- `GTH_DRY_RUN`: (Optional) Test eligibility without actually searching, `true|false`, default `false`.
- `GTH_INCLUDE_TAGS`: (Optional) Comma-separated list of tags. Items must have at least one matching tag, default empty (no filter).
- `GTH_EXCLUDE_TAGS`: (Optional) Comma-separated list of tags. Items with any matching tag are excluded, default empty (no filter).
- `GTH_MIN_MISSING_EPISODES`: (Optional) For Sonarr, minimum number of missing episodes required, default `0` (no threshold).
- `GTH_MIN_MISSING_PERCENT`: (Optional) For Sonarr, minimum percentage of missing episodes required (0.0-100.0), default `0.0` (no threshold).

### Per-target configuration

- `GTH_ARR_<n>_TYPE`: (Required) `radarr|sonarr`.
- `GTH_ARR_<n>_NAME`: (Required) instance identifier for logging.
- `GTH_ARR_<n>_BASEURL`: (Required) base URL for the Radarr/Sonarr instance (e.g., `http://radarr:7878`).
- `GTH_ARR_<n>_APIKEY`: (Required) API key for the instance.
- `GTH_ARR_<n>_OPS_PER_INTERVAL`: (Optional) Override.
- `GTH_ARR_<n>_INTERVAL_S`: (Optional) Override.
- `GTH_ARR_<n>_ITEM_REVISIT_S`: (Optional) Override.
- `GTH_ARR_<n>_REQUIRE_MONITORED`: (Optional) Override.
- `GTH_ARR_<n>_REQUIRE_CUTOFF_UNMET`: (Optional) Override.
- `GTH_ARR_<n>_RELEASED_ONLY`: (Optional) Override.
- `GTH_ARR_<n>_SEARCH_BACKOFF_S`: (Optional) Override.
- `GTH_ARR_<n>_DRY_RUN`: (Optional) Override.
- `GTH_ARR_<n>_INCLUDE_TAGS`: (Optional) Override.
- `GTH_ARR_<n>_EXCLUDE_TAGS`: (Optional) Override.
- `GTH_ARR_<n>_MIN_MISSING_EPISODES`: (Optional) Override.
- `GTH_ARR_<n>_MIN_MISSING_PERCENT`: (Optional) Override.

## Metrics

When `GTH_METRICS_ENABLED` is `true`, Gatherarr exposes a Prometheus-compatible endpoint at `/metrics` on the configured port. The following metrics are exported:

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `gatherarr_run_total` | Counter | Total number of scheduler runs | `target`, `type` (radarr/sonarr), `status` (success/error) |
| `gatherarr_requests_total` | Counter | Total number of *arr API requests (item searches) | `target`, `type` |
| `gatherarr_request_errors_total` | Counter | Total number of failed API requests | `target`, `type` |
| `gatherarr_grabs_total` | Counter | Total number of items searched (grabs) | `target`, `type` |
| `gatherarr_skips_total` | Counter | Total number of items skipped (eligibility/backoff) | `target`, `type` |
| `gatherarr_request_duration_seconds` | Histogram | Duration of search requests in seconds (buckets: 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0) | `target`, `type` |
| `gatherarr_last_success_timestamp_seconds` | Gauge | Unix timestamp of last successful run per target | `target`, `type` |
| `gatherarr_state_write_failures_total` | Counter | Total number of state file write failures | (none) |

## Goals and Non-Goals

### Goals

- Trigger Radarr and Sonarr searches on a configurable schedule.
- Support one or more Radarr/Sonarr instances.
- Persist minimal operational state to a single YAML file, and gracefully recover when state is reset or corrupted.
- Expose Prometheus-compatible metrics endpoint.
- Function properly when configured behind a firewall that limits outgoing network requests to only the configured *arr instances.

### Non-Goals

- No manual interaction.

### MVP

- Support for Radarr and Sonarr only.

## Security Notes

- **Hardened Docker Image**: Gatherarr uses a hardened Python 3.14 Docker image from Docker Hardened Images (DHI) for enhanced security. The hardened image provides additional security hardening, minimal attack surface, and follows security best practices. Vulnerability scan results for published images are available on the [Docker Hub image page](https://hub.docker.com/r/astrocatcmdr/gatherarr).
- `API_KEY` values are redacted from structured log statements and emitted as `[REDACTED]`.
- Gatherarr serves `/metrics` without built-in authentication when metrics are enabled. If authentication is required, place Gatherarr behind an external authentication or authorization layer (for example, a reverse proxy with auth controls) and/or network-level access controls.
- Gatherarr sends `X-Api-Key` to each configured `*arr` target. If `GTH_ARR_<n>_BASEURL` uses `http://` instead of `https://`, that API key is transmitted in cleartext over the network.
- A firewall may be used to limit outgoing network requests to only the configured *arr application URLs.

## Development

- The only supported development environment is the provided devcontainer.
- Keep commits focused and traceable to `PRD.md` requirements.
- Commits are only accepted via GitHub pull requests, which are welcome.

### Setup

Attach to the included devcontainer, and run

```bash
uv sync
```

### Verifying changes

- Incremental: `uv run poe check`
- Before PR: `uv run poe check-e2e`
