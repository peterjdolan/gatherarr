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
5. `uv run poe test`

## Run Commands

- Run app locally: `uv run python -m app`
- Full quality gate: `uv run poe check`
- Targeted tests: `uv run pytest tests/test_<area>.py`

## Coding Rules (Repository Standards)

- Do not introduce global state.
- Do not accept `None` or optional arguments in new interfaces; rely on strict typing and explicit required parameters.
- Avoid `cast`; keep interfaces strict enough for static typing without casts.
- Keep imports at module top level.
- Do not use defensive import patterns (`try/except ImportError`).
- Do not log secrets (API keys, tokens, or auth headers).
- Keep INFO logs structured and action-oriented.

## Testing Rules

- Do not use mocks (`unittest.mock`, `pytest-mock`, etc.).
- Use dependency injection for collaborators.
- Use fake objects implementing the same interface/protocol as production dependencies.
- Prefer targeted tests first, then broader checks when needed.
- When scheduler/state/retry/config logic changes, run the relevant focused tests plus `uv run poe type-check`.

## Change Guidance

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
- If you change any user-facing UI in this repo in the future, include a manual verification artifact (screenshot or video).

