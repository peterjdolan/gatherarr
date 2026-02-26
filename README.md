# Gatherarr

A lightweight service that performs one job: periodically trigger searches in supported *arr apps.

Huntarrs are great, but when you need a calm, reliable, and simple helper, you need a Gatherarr.

- **Goal:** Simple, reliable, observable background searches for *arr apps.
- **Deployment model:** Docker container only.
- **Configuration model:** Environment variables only. `.env` files and Docker Secrets may be used to manage configuration and API keys.
- **Security model:** No sensitive information written to disk or emitted in logs. No outgoing network requests except to the configured *arr servers. No telemetry or monitoring.

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

To manage more complex configurations, Docker `.env` files may be used. To securely handle sensitive API keys, Docker Secrets may be used.

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
- `GTH_ITEM_REVISIT_S`: (Optional) Minimum time in seconds to wait before reprocessing a previously processed item, default `604800` (one week).

### Per-target configuration

- `GTH_ARR_<n>_TYPE`: (Required) `radarr|sonarr`.
- `GTH_ARR_<n>_NAME`: (Required) instance identifier for logging.
- `GTH_ARR_<n>_BASEURL`: (Required) base URL for the Radarr/Sonarr instance (e.g., `http://radarr:7878`).
- `GTH_ARR_<n>_APIKEY`: (Required) API key for the instance.
- `GTH_ARR_<n>_OPS_PER_INTERVAL`: (Optional) override.
- `GTH_ARR_<n>_INTERVAL_S`: (Optional) override.
- `GTH_ARR_<n>_ITEM_REVISIT_TIMEOUT_S`: (Optional) override.

## Goals and Non-Goals

### Goals

- Trigger Radarr and Sonarr searches on a configurable schedule.
- Support one or more Radarr/Sonarr instances.
- Persist minimal operational state to a single JSON or YAML file, and gracefully recover when state is reset or corrupted.
- Expose Prometheus-compatible metrics endpoint.
- Function properly when configured behind a firewall that limits outgoing network requests to only the configured *arr instances.

### Non-Goals

- No manual interaction.
- No telemetry.

### MVP

- Support for Radarr and Sonarr only.

## Security Notes

- **Hardened Docker Image**: Gatherarr uses a hardened Python 3.14 Docker image from Docker Hardened Images (DHI) for enhanced security. The hardened image provides additional security hardening, minimal attack surface, and follows security best practices.
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

### Verifying a change

After incremental changes..

```bash
uv run poe check
```

Before submitting a PR..

```bash
uv run poe check-e2e
```
