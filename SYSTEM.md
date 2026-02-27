# SYSTEM.md — Gatherarr System Architecture

This document describes the system architecture, design decisions, and operational considerations for Gatherarr. It complements [PRD.md](PRD.md) (product requirements) and [AGENTS.md](AGENTS.md) (coding guidelines).

## Overview

Gatherarr is a worker-style daemon that periodically triggers search operations in *arr services (Radarr, Sonarr). It runs as a long-lived process, scheduling runs per target, fetching items, applying eligibility filters, triggering searches, and persisting state.

**Core invariants:**

- Configuration comes from environment variables only; no file-based config.
- All initialization happens once in `app/main.py`; no global accessors.
- Dependencies are passed explicitly; modules do not read environment variables.
- State is minimal and persisted to a single YAML file with atomic writes.

## Component Architecture

```mermaid
flowchart TD
    Main["app/main.py<br>load_config, StateManager, ArrClient<br>Scheduler, Flask /health /metrics<br>Signal handling"]
    Config["app/config.py<br>load_config, Config, ArrTarget"]
    State["app/state.py<br>StateManager, StateStorage<br>File / InMemory"]
    Scheduler["app/scheduler.py<br>run_once, _process_items<br>ItemHandler dispatch"]
    Handlers["app/handlers<br>MovieHandler, SeasonHandler"]
    ArrClient["app/arr_client<br>ArrClient<br>get_movies, get_seasons<br>search_movie, search_season"]
    HttpClient["app/http_client<br>HttpxClient, HttpClient"]

    Main --> Config
    Main --> State
    Main --> Scheduler
    Scheduler --> Handlers
    Scheduler --> ArrClient
    ArrClient --> HttpClient
```

### Main Module (`app/main.py`)

The single entry point. Responsibilities:

1. **Load config** — `load_config()` reads environment variables, validates, and builds `Config`. Fails fast on validation errors.
2. **Setup logging** — Structured JSON logging via structlog; sensitive fields redacted.
3. **State** — Chooses `FileStateStorage` or `InMemoryStateStorage` (when `state_file_path` is None). Loads state on startup.
4. **HTTP and Arr clients** — Creates a shared `httpx.AsyncClient` and `HttpxClient` wrapper; one `ArrClient` per target.
5. **Scheduler** — Starts async scheduler loop. Runs until shutdown signal.
6. **Web server** — When metrics enabled, Flask serves `/health` and `/metrics` in a daemon thread.
7. **Shutdown** — On SIGTERM/SIGINT: stop scheduler, cancel task, close HTTP client.

**Assumption:** The process runs in a container; `state_file_path` is typically a mounted volume. No root required.

### Configuration (`app/config.py`)

- **Source:** Environment variables with `GTH_` prefix. No config files.
- **Validation:** Fail fast on missing required vars, invalid values, unrecognized `GTH_*` keys (typo detection).
- **Target discovery:** Sequential indices `GTH_ARR_0_*`, `GTH_ARR_1_*`, … until `GTH_ARR_n_TYPE` is missing.
- **Per-target overrides:** `TargetSettings` inherit from global defaults; overrides applied per index.
- **Duplicate names:** PRD requires rejection of duplicate target names (validation in load).

**Design decision:** Reject unrecognized `GTH_*` variables to surface typos and obsolete config early.

### Scheduler (`app/scheduler.py`)

- **Loop:** Every 1 second, checks which targets are due (based on `interval_s` since last run). Runs due targets concurrently via `asyncio.gather`.
- **Per-target run:** Fetches items via `ArrClient`, selects handler by target type (Radarr → MovieHandler, Sonarr → SeasonHandler), processes items via `ItemHandler` protocol.
- **Item processing order:** Extract logging ID → extract item ID → state/backoff checks → eligibility (`should_search`) → search (or dry-run).
- **Metrics:** Updates `run_total`, `grabs_total`, `skips_total`, `request_errors_total`, etc.
- **State:** Persists after each run; increments `total_runs`.

**Assumption:** Handler is selected by `ArrType`; scheduler has no item-type-specific logic beyond handler dispatch.

### ItemHandler Protocol and Handlers

The scheduler delegates all item-type logic to `ItemHandler` implementations. This keeps the scheduler generic and supports Fake implementations for tests.

#### ItemId

Item identifiers extend `ItemId`:

- `format_for_state() -> str` — Deterministic key for state lookup (e.g. `"42"` for movies, `"123:4"` for series/season).
- `logging_ids() -> dict[str, Any]` — Correlation fields for logs (`movie_id`, `movie_name` or `series_id`, `season_number`, `series_name`).

#### ItemHandler Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `extract_item_id(item)` | ID for state and revisit timing | `ItemId \| None` |
| `extract_logging_id(item)` | Logging correlation dict | `dict[str, str]` |
| `should_search(item, logging_ids)` | Eligibility rules (monitored, cutoff, tags, etc.) | `bool` |
| `search(client, item, logging_ids)` | Trigger search and log action | `None` (async) |

**Call order:** `extract_logging_id` → `extract_item_id` → state/backoff checks → `should_search` → `search`.

**Extensibility:** New *arr apps (e.g. Lidarr) require a handler, an `ItemId` subclass, and ArrClient search methods. Scheduler only needs to map the new type to its handler.

### ArrClient (`app/arr_client.py`)

- **HTTP layer:** Uses `HttpClient` protocol (injected; real impl: `HttpxClient`).
- **Retries:** Tenacity for network errors, timeouts, 5xx, 429. Configurable max attempts, delay, backoff.
- **Auth:** `X-Api-Key` header per target.
- **Endpoints:** Radarr `GET /api/v3/movie`, `POST /api/v3/command` (MoviesSearch); Sonarr `GET /api/v3/series`, flatten to seasons, `POST /api/v3/command` (SeasonSearch).

**Assumption:** *arr API contracts (JSON shape, field names) are stable; no defensive type checks per AGENTS.md.

### State (`app/state.py`)

- **Model:** `State` → `targets[name]` → `TargetState` → `items[item_id]` → `ItemState`.
- **Persistence:** `StateStorage` protocol. `FileStateStorage` uses atomic write (temp file → fsync → rename).
- **Corruption:** On YAML parse or deserialization error, move file to `.corrupt.<timestamp>`, start fresh.
- **Size cap:** PRD specifies 10 MB cap; prune oldest item state when exceeded (planned).

**Design decision:** Atomic write ensures no partial state on crash. Corrupt files are preserved for debugging.

### Logging and Metrics

- **Structured logs:** structlog, JSON to stdout/stderr. Correlation fields: `target_name`, `target_type`, `run_id`, `movie_id`/`series_id`/`season_number`.
- **Redaction:** `log_redaction.redact_sensitive_fields` removes `api_key`, `apikey`, `x-api-key`, etc. from all log output.
- **Log levels:** INFO for actions that affect targets (searches); DEBUG for fetches, internal steps.
- **Metrics:** Prometheus counters/gauges/histograms; served on `/metrics` when enabled.

## Design Decisions and Assumptions

### Single Initialization Point

All config, state, and client setup happens in `main()`. No module reads env vars or uses global accessors. This simplifies testing (inject config) and reasoning about startup order.

### Explicit Dependency Injection

`ArrClient` receives `HttpClient`; `Scheduler` receives `StateManager` and `arr_clients`; handlers receive `ArrTarget`. Fakes replace real implementations in tests without mocks.

### No Defensive API Checks

Per AGENTS.md, we do not add checks like `isinstance(x, bool)` when expecting `int`. Incorrect assumptions about *arr responses should surface as exceptions, not silent misbehavior.

### Configuration Strictness

Unrecognized `GTH_*` variables cause startup failure. This avoids silent typos and forces cleanup of obsolete config.

## Security

- **Container:** The image runs as a non-root user with no privileged operations; this is an architectural constraint of the deployment model.

## Robustness

- **HTTP retries:** Network errors, 5xx, 429 retried with exponential backoff. Non-retryable errors (e.g. 4xx) fail immediately.
- **State corruption:** Recovered by moving corrupt file aside and starting fresh. No partial state loaded.
- **Shutdown:** Scheduler stops; in-flight work completes or is cancelled. HTTP client closed cleanly.
- **Graceful shutdown:** PRD v0.1 adds configurable `shutdown_timeout_s` to cap shutdown duration.

## Testability

- **Fake objects:** `FakeArrClient`, `FakeClientWithError`, `InMemoryStateStorage` implement protocols. Tests inject them.
- **No mocks:** Per AGENTS.md, prefer Fakes over `unittest.mock`. Fakes are configurable (e.g. raise error, return ineligible items).
- **Config injection:** `load_config(env=...)` accepts a dict for deterministic tests.
- **Protocols:** `ItemHandler`, `StateStorage`, `HttpClient` enable substitution without changing production code.

## Extensibility

- **New *arr apps:** Add `ArrType`, handler, `ItemId` subclass, ArrClient methods. Wire handler in scheduler by type.
- **New eligibility rules:** Implement in handler `should_search`; scheduler unchanged.
- **New storage:** Implement `StateStorage`; `StateManager` unchanged.
