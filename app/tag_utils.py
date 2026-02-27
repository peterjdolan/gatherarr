"""Utilities for normalizing and filtering item tags."""

from collections.abc import Iterable


def normalize_tag_set(raw_tags: Iterable[object]) -> set[str]:
  """Normalize raw tag values into a stripped, de-duplicated set."""
  return {normalized_tag for raw_tag in raw_tags if (normalized_tag := str(raw_tag).strip())}


def parse_csv_tag_set(raw_csv: str) -> set[str]:
  """Parse a comma-separated tag string into a normalized set."""
  return normalize_tag_set(raw_csv.split(","))


def coerce_tag_set(raw_value: object) -> set[str]:
  """Coerce a CSV string or iterable tags into a normalized set."""
  if isinstance(raw_value, str):
    return parse_csv_tag_set(raw_value)
  if isinstance(raw_value, (list, set, tuple)):
    return normalize_tag_set(raw_value)
  if raw_value is None:
    return set()
  raise ValueError("tags must be a CSV string, list, tuple, or set")


def extract_item_tags(item: dict[str, object]) -> set[str]:
  """Extract and normalize tags from an item payload."""
  raw_tags = item.get("tags")
  if isinstance(raw_tags, (list, set, tuple)):
    return normalize_tag_set(raw_tags)
  return set()


def tag_filter(item_tags: set[str], include_tags: set[str], exclude_tags: set[str]) -> bool:
  """Return True when item tags pass include/exclude constraints."""
  if include_tags and item_tags.isdisjoint(include_tags):
    return False
  return item_tags.isdisjoint(exclude_tags)
