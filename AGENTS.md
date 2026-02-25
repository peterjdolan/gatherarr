# Gatherarr

A lightweight Python daemon that periodically triggers searches in Radarr/Sonarr *arr apps.

## Cursor Cloud specific instructions

### Project overview

Single-service Python 3.13 application. No databases, no Docker required for development. All tests are self-contained using fake implementations (no mocks, no external services).

### Key commands

All tasks run via `uv run poe <task>` (poethepoet). See `[tool.poe.tasks]` in `pyproject.toml` for the full list:

- `uv run poe check` — runs format + lint + type-check + test (full CI equivalent)
- `uv run poe test` — pytest only (127 unit tests, ~2s)
- `uv run poe type-check` — mypy strict mode
- `uv run poe lint-check` — ruff lint (read-only)
- `uv run poe format-check` — ruff format (read-only)

### Running the application locally

The app requires `GTH_ARR_*` environment variables. Minimal example:

```bash
GTH_METRICS_ENABLED=true \
GTH_ARR_0_TYPE=radarr \
GTH_ARR_0_NAME=TestRadarr \
GTH_ARR_0_BASEURL=http://localhost:7878 \
GTH_ARR_0_APIKEY=test-api-key \
GTH_STATE_FILE_PATH="" \
PYTHONPATH=/workspace \
uv run python app/main.py
```

Health: `http://localhost:9090/health` — Metrics: `http://localhost:9090/metrics`

Setting `GTH_STATE_FILE_PATH=""` uses in-memory state (avoids needing `/data/` directory). The scheduler will log errors connecting to Radarr/Sonarr if no real instance is available; this is expected in dev.

### Caveats

- Python 3.13 is required (`>=3.13,<3.14`). The VM ships with 3.12, so the update script installs 3.13 from the deadsnakes PPA.
- `uv` must be on `PATH` (installed to `~/.local/bin`).
- `PYTHONPATH=/workspace` is needed when running `app/main.py` directly; `uv run poe` commands handle this automatically.
