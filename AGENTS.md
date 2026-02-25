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

- Python version: `>=3.13,<3.14`.
- Dependency manager and runner: `uv`.
- Task runner: `poethepoet` (`poe` tasks in `pyproject.toml`).

Setup:

1. `uv sync --dev`
2. `uv run poe format-check`
3. `uv run poe lint-check`
4. `uv run poe type-check`
5. `uv run poe check`
6. `uv run poe test-e2e`

## Run Commands

- Run app locally: `uv run python -m app`
- Run base tests (excluding integration tests): `uv run poe test`
- Run integration tests: `uv run poe test-e2e`
- Full quality gate (base checks only): `uv run poe check`
- Full quality gate (base + integration checks): `uv run poe check-e2e`
- Targeted tests: `uv run pytest tests/test_<area>.py`

## Architecture Rules (Migrated from `.cursor/rules/architecture.mdc`)

### Backwards Compatibility

- **DO NOT maintain backwards compatibility** - Feel free to refactor, rename, or restructure code as needed.
- **ALWAYS write clean, maintainable code** - Do not preserve old interfaces or patterns when a simpler option could be implemented.

### Initialization and Configuration

- **Single initialization point** - All module initialization (config parsing, database connections, etc.) must happen once and only once in the main module (for example, `app/main.py` lifespan function).
- **NO global accessor methods** - Do not create global accessor functions that read from environment variables or global state.
- **Pass dependencies explicitly** - Parse configuration once in the main module and pass the config object explicitly to every code path that needs it.
- **Configuration as parameter** - Functions that need configuration should accept it as a parameter rather than calling a global accessor.
- **No environment variable access in modules** - Only the main module should read environment variables; all other modules receive configuration through function or constructor parameters.

## Coding Patterns (Migrated from `.cursor/rules/style.mdc`)

- DO NOT accept `None` or optional arguments. DO NOT test for whether or not an argument is `None` or contains `None` values. Rely on type checking to ensure that all parameters are valid. Maintain a strict expectation that function calls always use exactly the expected parameters.
- AVOID using `cast` whenever possible. Rely on type checking to maintain strict API expectations and avoid runtime errors.
- **DO NOT use any global state**.

### Testing Patterns

- **DO NOT use mocks** (`unittest.mock`, `pytest-mock`, etc.) in tests.
- **USE dependency injection** - Design code to accept dependencies via constructor parameters. Initialize the dependencies ONLY in the application's main method.
- **USE Fake objects** - Create Fake implementations of interfaces/protocols for testing.
- Fake objects should implement the same interface as real objects.
- Fake objects should be configurable to simulate different scenarios (success, errors, edge cases).

### Imports

- **NO defensive imports** - Do not use `try/except` blocks for imports. Assume all required dependencies are installed and available. If a dependency is optional, it should be documented in project dependencies or configuration, not handled with defensive imports.
- **All imports at top** - All imports must be at the top of the module. Do not import anything inline within methods or functions.

## Testing Execution Rules (Migrated from `.cursor/rules/testing.mdc`)

### Running Code Checks

- Always use `uv run poe check` to run base code quality checks (formatting/lint/type-check/base tests).
- Always use `uv run poe check-e2e` when you need base checks plus integration tests.

### Running Tests

- Use `uv run poe test` for base tests only (`tests/integration` is excluded).
- Use `uv run poe test-e2e` for integration tests in `tests/integration`.

### Before Committing Code

Before suggesting code changes are complete:

1. Run `uv run poe check` to ensure base checks pass.
2. If checks fail, fix issues before proceeding.
3. Ensure integration tests pass with `uv run poe test-e2e`.

### When Making Code Changes

- After making code changes, verify they pass linting and type checks.
- Ensure new code includes appropriate tests.
- Run `uv run poe check` at minimum.
- Run `uv run poe test-e2e` whenever integration behavior is affected.

### Test Configuration Files

- **Reference examples** - Test configuration files serve as reference examples for users, so they should be complete, valid, and demonstrate proper configuration patterns.
- **Documentation** - Test configuration files should include comments explaining their purpose and any test-specific requirements.

## Additional Repository Guidance

- Do not log secrets (API keys, tokens, or auth headers).
- Keep INFO logs structured and action-oriented.
- Keep changes small and traceable to `PRD.md` requirements.
- Update tests alongside behavior changes.
- Prefer explicit, deterministic behavior over hidden defaults.
- Preserve environment-variable-first configuration.

## Cursor Cloud specific instructions

- Start by reading `AGENTS.md`, `README.md`, and `PRD.md`.
- Use the smallest high-signal test set for touched code; avoid running unrelated large suites.
- For non-trivial changes, run at minimum:
  - `uv run poe lint-check`
  - `uv run poe type-check`
  - impacted `uv run pytest ...` targets
- Run `uv run poe check` for broad or cross-cutting changes.
- Run `uv run poe test-e2e` for integration coverage.
- If you change any user-facing UI in this repo in the future, include a manual verification artifact (screenshot or video).
