# AGENTS.md

## Testing commands

- Run base tests (excluding integration tests): `uv run poe test`
- Run integration tests: `uv run poe test-e2e`
- Run full quality checks without integration tests: `uv run poe check`
- Run full quality checks including integration tests: `uv run poe check-e2e`

## Before committing

- Always run `uv run poe check` for formatting, linting, type checks, and base tests.
- Always run `uv run poe test-e2e` to validate integration coverage.
