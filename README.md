# Gatherarr

A lightweight service that performs one job: periodically trigger searches in supported *arr apps.

Huntarrs are great, but when you need a calm, reliable, and simple helper, you look for a Gatherarr.

- **Primary value:** simple, reliable, observable automated search triggering
- **Deployment model:** Docker container only
- **Configuration model:** environment variables only (no UI, no CLI config files)

## Minimal Deployment

```bash
git clone https://github.com/peterjdolan/gatherarr.git
```

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
```

```bash
docker compose up --build gatherarr
```

## Docker Hub Image Publishing (GitHub Actions)

The repository publishes images to Docker Hub at `astrocatcmdr/gatherarr` using `.github/workflows/docker-image.yml`.

To enable pushes from GitHub Actions, configure these repository secrets:

- `DOCKERHUB_USERNAME`: Docker Hub account name (for this repository, `astrocatcmdr`)
- `DOCKERHUB_TOKEN`: Docker Hub access token with write access to `astrocatcmdr/gatherarr`

Pull the published image with:

```bash
docker pull astrocatcmdr/gatherarr:latest
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

### Per-target configuration

- `GTH_STATE_FILE_PATH`: (Optional) path to state persistence file, default `/data/state.yaml`.
- `GTH_ARR_<n>_TYPE`: (Required) `radarr|sonarr`.
- `GTH_ARR_<n>_NAME`: (Required) instance identifier.
- `GTH_ARR_<n>_BASEURL`: (Required) base URL for the Radarr/Sonarr instance (e.g., `http://radarr:7878`).
- `GTH_ARR_<n>_APIKEY`: (Required) API key for the instance.
- `GTH_ARR_<n>_OPS_PER_INTERVAL`: (Optional override) Maximum number of operations to perform per interval.
- `GTH_ARR_<n>_INTERVAL_S`: (Optional override) Interval in seconds.
- `GTH_ARR_<n>_ITEM_REVISIT_TIMEOUT_S`: (Optional override) Minimum number of seconds to wait before reprocessing a previously processed item for this instance.

## Development

- The only supported development environment is the provided devcontainer.
- Use pull requests for all changes.
- Keep commits focused and traceable to `PRD.md` requirements.
- Commits are only accepted via pull requests, which are welcome.
