"""Tests for tag utility helpers."""

from app.tag_utils import coerce_tag_set, extract_item_tags, parse_csv_tag_set, tag_filter


class TestTagUtils:
  def test_parse_csv_tag_set_deduplicates_and_strips(self) -> None:
    """CSV parsing should deduplicate and remove empty tags."""
    result = parse_csv_tag_set(" 4k, hdr,4k, , ")
    assert result == {"4k", "hdr"}

  def test_coerce_tag_set_handles_iterables(self) -> None:
    """Coercion should normalize tags from iterable values."""
    result = coerce_tag_set(["anime", " anime ", "", "uhd"])
    assert result == {"anime", "uhd"}

  def test_extract_item_tags_handles_missing_tags(self) -> None:
    """Missing tags field should yield an empty set."""
    assert extract_item_tags({"id": 1}) == set()

  def test_tag_filter(self) -> None:
    """Filter should enforce include and exclude tag sets."""
    item_tags = {"anime", "uhd"}
    assert tag_filter(item_tags, include_tags={"anime"}, exclude_tags={"skip"}) is True
    assert tag_filter(item_tags, include_tags={"drama"}, exclude_tags={"skip"}) is False
    assert tag_filter(item_tags, include_tags={"anime"}, exclude_tags={"uhd"}) is False
