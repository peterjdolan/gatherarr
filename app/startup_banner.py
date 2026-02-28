"""Startup banner for configuration display."""

from app.config import ArrTarget, Config

REDACTED = "[REDACTED]"


def _format_tags(value: str | set[str]) -> str:
  """Format tags (str or set) for display."""
  if isinstance(value, set):
    return ", ".join(sorted(value)) if value else "(none)"
  return value if value else "(none)"


def _format_target(target: ArrTarget, index: int) -> str:
  """Format a single target for banner display."""
  s = target.settings
  lines = [
    f"  [{index}] {target.name} ({target.arr_type})",
    f"    base_url: {target.base_url}",
    f"    api_key: {REDACTED}",
    f"    ops_per_interval: {s.ops_per_interval}",
    f"    interval_s: {s.interval_s}",
    f"    item_revisit_s: {s.item_revisit_s}",
    f"    require_monitored: {s.require_monitored}",
    f"    require_cutoff_unmet: {s.require_cutoff_unmet}",
    f"    released_only: {s.released_only}",
    f"    search_backoff_s: {s.search_backoff_s}",
    f"    dry_run: {s.dry_run}",
    f"    include_tags: {_format_tags(s.include_tags)}",
    f"    exclude_tags: {_format_tags(s.exclude_tags)}",
    f"    min_missing_episodes: {s.min_missing_episodes}",
    f"    min_missing_percent: {s.min_missing_percent}",
  ]
  return "\n".join(lines)


def format_banner(config: Config) -> str:
  """Format full configuration as an easily readable startup banner."""
  state_path = config.state_file_path if config.state_file_path else "(in-memory)"
  global_lines = [
    "=== Gatherarr Startup Configuration ===",
    "",
    "Global:",
    f"  log_level: {config.log_level}",
    f"  metrics_enabled: {config.metrics_enabled}",
    f"  metrics_address: {config.metrics_address}",
    f"  metrics_port: {config.metrics_port}",
    f"  state_file_path: {state_path}",
    f"  ops_per_interval: {config.ops_per_interval}",
    f"  interval_s: {config.interval_s}",
    f"  item_revisit_s: {config.item_revisit_s}",
    f"  require_monitored: {config.require_monitored}",
    f"  require_cutoff_unmet: {config.require_cutoff_unmet}",
    f"  released_only: {config.released_only}",
    f"  search_backoff_s: {config.search_backoff_s}",
    f"  dry_run: {config.dry_run}",
    f"  include_tags: {_format_tags(config.include_tags)}",
    f"  exclude_tags: {_format_tags(config.exclude_tags)}",
    f"  min_missing_episodes: {config.min_missing_episodes}",
    f"  min_missing_percent: {config.min_missing_percent}",
    "",
    "Targets:",
  ]
  target_blocks = [_format_target(t, i) for i, t in enumerate(config.targets)]
  return "\n".join(global_lines + target_blocks)
