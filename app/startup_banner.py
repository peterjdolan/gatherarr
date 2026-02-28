"""Startup banner for configuration display."""

from app.config import ArrTarget, Config

REDACTED = "[REDACTED]"

_TAG_FIELDS = frozenset({"include_tags", "exclude_tags"})


def _format_value(key: str, value: object) -> str:
  """Format a config value for display."""
  if key in _TAG_FIELDS:
    if isinstance(value, set):
      return ", ".join(sorted(value)) if value else "(none)"
    if isinstance(value, list):
      return ", ".join(sorted(value)) if value else "(none)"
    return str(value) if value else "(none)"
  return str(value)


def _format_section(data: dict[str, object], indent: str = "  ") -> list[str]:
  """Format a section of key-value pairs for banner display."""
  return [f"{indent}{k}: {_format_value(k, v)}" for k, v in data.items()]


def _format_target(target: ArrTarget, index: int) -> str:
  """Format a single target for banner display."""
  header = f"  [{index}] {target.name} ({target.arr_type})"
  # Build target attributes: name/arr_type in header, base_url, api_key (redacted), then settings
  target_attrs: dict[str, object] = {
    "base_url": target.base_url,
    "api_key": REDACTED,
  }
  settings_data = target.settings.model_dump(mode="json")
  target_attrs.update(settings_data)
  lines = [header] + _format_section(target_attrs, indent="    ")
  return "\n".join(lines)


def format_banner(config: Config) -> str:
  """Format full configuration as an easily readable startup banner."""
  global_data: dict[str, object] = {}
  for name in Config.model_fields:
    if name == "targets":
      continue
    value = getattr(config, name)
    if name == "state_file_path" and (value is None or value == ""):
      value = "(in-memory)"
    global_data[name] = value
  global_lines = [
    "=== Gatherarr Startup Configuration ===",
    "",
    "Global:",
  ] + _format_section(global_data)
  target_blocks = [_format_target(t, i) for i, t in enumerate(config.targets)]
  return "\n".join(global_lines + ["", "Targets:"] + target_blocks)
