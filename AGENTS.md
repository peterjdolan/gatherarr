# AGENTS.md

## Purpose

This file provides repository-specific instructions for coding agents working in this project.

## Project Snapshot

- Project: `gatherarr` (worker-style daemon for periodic Radarr/Sonarr search triggering).
- Runtime model: Docker container deployment.
- Configuration model: environment variables only.
- Main package: `app/`.
- Tests: `tests/`.
- Product requirements: `PRD.md`.

## Environment and Tooling

- Python version: `==3.14`.
- Dependency manager and runner: `uv`.
- Task runner: `poethepoet` (`poe` tasks in `pyproject.toml`).

## Run Commands

- Run app locally: `uv run python -m app`
- Targeted tests: `uv run pytest tests/test_<area>.py`
- Incremental quality gate: `uv run poe check`
- Full quality gate: `uv run poe check-e2e`

## Architecture Rules

### Backwards Compatibility

- **DO NOT maintain backwards compatibility** - Feel free to refactor, rename, or restructure code as needed.
- **ALWAYS write clean, maintainable code** - Do not preserve old interfaces or patterns when a simpler option could be implemented.

### Initialization and Configuration

- **Single initialization point** - All module initialization (config parsing, database connections, etc.) must happen once and only once in the main module (`app/main.py`).
- **NO global accessor methods** - Do not create global accessor functions that read from environment variables or global state.
- **Pass dependencies explicitly** - Parse configuration once in the main module and pass the config object explicitly to every code path that needs it.
- **Configuration as parameter** - Functions that need configuration should accept it as a parameter rather than calling a global accessor.
- **No environment variable access in modules** - Only the main module should read environment variables; all other modules receive configuration through function or constructor parameters.

## Coding Patterns

- **NO global state** - DO NOT create or access global state. DO read from environment variables. DO NOT create or modify environment variables.
- **Strict type safety** - AVOID using `cast` whenever possible. Rely on type checking to maintain strict API expectations and avoid runtime errors.

### Testing Patterns

- **AVOID using mocks** (`unittest.mock`, `pytest-mock`, etc.) in tests.
- **USE dependency injection** - Design code to accept dependencies via constructor parameters. Initialize the dependencies ONLY in the application's main method.
- **USE Fake objects** - Create Fake implementations of interfaces/protocols for testing.
- Fake objects should implement the same interface as real objects. Write tests that verify that Fake objects APIs match the classes they are faking.
- Fake objects should be configurable to simulate different scenarios (success, errors, edge cases).

### Imports

- **NO defensive imports** - Do not use `try/except` blocks for imports. Assume all required dependencies are installed and available. If a dependency is optional, it should be documented in project dependencies or configuration, not handled with defensive imports.
- **All imports at top** - All imports must be at the top of the module. Do not import anything inline within methods or functions.

### Security

- Do not log secrets (API keys, tokens, or auth headers). If any new sensitive information is introduced, ensure it's redacted by the log redaction utilities in `app/log_redaction.py`

### Logging

- All actions that materially impact external systems (*arr apps) must be logged at the INFO level with all necessary contextual information. For example, executing searches for movies or series must be logged at INFO level. Requesting the list of movies from a Radarr instance should be logged at DEBUG level.
- All logs should have all necessary contextual information included in the logger statement.
- All exceptions should be logged at ERROR level with `logger.exception`.

## Testing Execution Rules

### Running Code Checks

- Always use `uv run poe check` to run base code quality checks (formatting/lint/type-check/base tests).
- Always use `uv run poe check-e2e` when you need base checks plus integration tests.

### Running Tests

- Use `uv run poe test` for base tests only (`tests/integration` is excluded).
- Use `uv run poe test-e2e` for integration tests in `tests/integration`.

### Before Committing Code

Before suggesting code changes are complete:

1. Run `uv run poe check` to ensure all checks pass.
1. If checks fail, fix issues before proceeding.
1. As a last check before a commit, ensure integration tests pass with `uv run poe test-e2e`.

## Additional Repository Guidance

- Keep changes small and traceable to `PRD.md` requirements.
- Updated `PRD.md` to document new features, assumptions, architectural changes, and design decisions.
- Update tests alongside behavior changes.
- Prefer explicit, deterministic behavior over hidden defaults.
- Preserve environment-variable-first configuration.

## Cursor Cloud specific instructions

- Start by reading `AGENTS.md`, `README.md`, and `PRD.md`.
- Update `README.md` to document user-impacting details.
- Update `PRD.md` to document product feature set, system architecture, and design decisions.
- Update `AGENTS.md` to document coding style and agent instructions.
- Use the smallest high-signal test set for touched code; avoid running unrelated large suites.
- For non-trivial changes, run at minimum `uv run poe check` to verify code formatting, type safety, and the unit test suite.
- Run `uv run poe check-e2e` for broad or cross-cutting changes.

### Environment caveats

- The correct app entrypoint is `uv run python -m app.main` (not `uv run python -m app`; the package has no `__main__.py`).
- Running the app locally requires `GTH_ARR_<n>_*` env vars and a writable state directory. Use `GTH_STATE_FILE_PATH=/tmp/gatherarr-data/state.yaml` (after `mkdir -p /tmp/gatherarr-data`) to avoid the default `/data/state.yaml` which requires a Docker volume.
- The Cloud VM ships with Rust/Cargo 1.83 which is too old to build `rpds-py`. The update script handles this by prepending the `rustup stable` toolchain to `PATH`. If builds fail with `edition2024` errors, run `rustup update stable`.
- No external services (Radarr, Sonarr, Docker, Prometheus) are needed for dev/test. All tests use in-process fakes and OpenAPI contract validation.
