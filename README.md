# Gatherarr

A lightweight service that performs one job: periodically trigger searches in supported *arr apps.

Huntarrs are great, but when you need a calm, reliable, and simple helper, you look for a Gatherarr.

- **Primary value:** simple, reliable, observable automated search triggering
- **Deployment model:** Docker container only
- **Configuration model:** environment variables only (no UI, no CLI config files)

## Minimal Deployment

1. Clone the repository:

```bash
git clone https://github.com/peterjdolan/gatherarr.git
```

2. Create `docker-compose.yaml` in the parent directory and adjust hostnames/API keys for your environment:

```yaml
services:
  gatherarr:
    build: ./gatherarr
    container_name: gatherarr
    environment:
      GTH_METRICS_ENABLED: true
      GTH_ARR_0_TYPE: radarr
      GTH_ARR_0_NAME: Radarr
      GTH_ARR_0_BASEURL: http://radarr:7878
      GTH_ARR_0_APIKEY: 059b34da8966442aab57fd2e3debfa9b
      GTH_ARR_1_TYPE: sonarr
      GTH_ARR_1_NAME: Sonarr
      GTH_ARR_1_BASEURL: http://sonarr:8989
      GTH_ARR_1_APIKEY: 71bc23f90cb44eb3a22d5d8b01f99e5b
```

3. Start Gatherarr:

```bash
docker compose up --build gatherarr
```

## Goals and Non-Goals

### Goals

- Trigger Radarr and Sonarr searches on a configurable schedule.
- Support one or more Radarr/Sonarr instances.
- Persist minimal operational state to a single JSON or YAML file, and gracefully recover when state is reset or corrupted.
- Expose Prometheus-compatible metrics endpoint.

### Non-Goals

- No manual interaction.

### MVP

- Support for Radarr and Sonarr only.

## Users and Use Cases

- **User:** self-hosters running Radarr/Sonarr who want periodic search execution.
- **Primary use case:** run searches every N minutes/hours with strict load control, safe retries, and monitoring visibility.

## Configuration

Configuration is done by environment variables only. Docker Compose users are welcome to use `.env` files for configuration management, and Docker Secrets to manage sensitive API tokens.

### Global configuration

- `GTH_LOG_LEVEL`: (Optional) log verbosity, `debug|info|warn|error`, default `info`.
- `GTH_METRICS_ENABLED`: (Optional) Whether or not to host the metrics endpoint (true/false).
- `GTH_METRICS_ADDRESS`: (Optional) Metrics endpoint listen address (default `0.0.0.0`).
- `GTH_METRICS_PORT`: (Optional) Metrics endpoint port (default 9090).
- `GTH_OPS_PER_INTERVAL`: (Optional) Common number of operations to perform per interval time, default 1.
- `GTH_INTERVAL_S`: (Optional) Common interval duration in seconds, default 60.
- `GTH_ITEM_REVISIT_S`: (Optional) Minimum time in seconds to wait before reprocessing a previously processed item. If not set, a default value is used (e.g., 86400 for 24 hours).
- `GTH_REQUIRE_MONITORED`: (Optional) Require items to be monitored before searching (default `true`).
- `GTH_REQUIRE_CUTOFF_UNMET`: (Optional) Require quality cutoff to be unmet before searching (default `true`).
- `GTH_RELEASED_ONLY`: (Optional) Search only released items (default `false`).
- `GTH_SEARCH_BACKOFF_S`: (Optional) Backoff seconds for retrying items after failed searches (default `0`, disabled).
- `GTH_DRY_RUN`: (Optional) Evaluate eligibility without triggering search commands (default `false`).
- `GTH_INCLUDE_TAGS`: (Optional) Comma-separated tags to include.
- `GTH_EXCLUDE_TAGS`: (Optional) Comma-separated tags to exclude.
- `GTH_MIN_MISSING_EPISODES`: (Optional, Sonarr-oriented) Minimum missing episodes required to search (default `0`).
- `GTH_MIN_MISSING_PERCENT`: (Optional, Sonarr-oriented) Minimum missing-episode percent required to search (default `0`).

### Per-target configuration

- `GTH_STATE_FILE_PATH`: (Optional) path to state persistence file, default `/data/state.yaml`.
- `GTH_ARR_<n>_TYPE`: (Required) `radarr|sonarr`.
- `GTH_ARR_<n>_NAME`: (Required) instance identifier.
- `GTH_ARR_<n>_BASEURL`: (Required) base URL for the Radarr/Sonarr instance (e.g., `http://radarr:7878`).
- `GTH_ARR_<n>_APIKEY`: (Required) API key for the instance.
- `GTH_ARR_<n>_OPS_PER_INTERVAL`: (Optional override) Maximum number of operations to perform per interval.
- `GTH_ARR_<n>_INTERVAL_S`: (Optional override) Interval in seconds.
- `GTH_ARR_<n>_ITEM_REVISIT_TIMEOUT_S`: (Optional override) Minimum number of seconds to wait before reprocessing a previously processed item for this instance.
- `GTH_ARR_<n>_REQUIRE_MONITORED`: (Optional override) Require monitored items only.
- `GTH_ARR_<n>_REQUIRE_CUTOFF_UNMET`: (Optional override) Require quality cutoff unmet.
- `GTH_ARR_<n>_RELEASED_ONLY`: (Optional override) Search only released items.
- `GTH_ARR_<n>_SEARCH_BACKOFF_S`: (Optional override) Backoff seconds after failed searches.
- `GTH_ARR_<n>_DRY_RUN`: (Optional override) Enable dry-run mode for this instance.
- `GTH_ARR_<n>_INCLUDE_TAGS`: (Optional override) Comma-separated tags that must match.
- `GTH_ARR_<n>_EXCLUDE_TAGS`: (Optional override) Comma-separated tags to skip.
- `GTH_ARR_<n>_MIN_MISSING_EPISODES`: (Optional override, Sonarr-oriented) Minimum missing episodes.
- `GTH_ARR_<n>_MIN_MISSING_PERCENT`: (Optional override, Sonarr-oriented) Minimum missing percentage.

## Development

- The only supported development environment is the provided devcontainer.
- Use pull requests for all changes.
- Keep commits focused and traceable to `PRD.md` requirements.
- Commits are only accepted via pull requests, which are welcome.
