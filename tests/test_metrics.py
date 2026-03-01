"""Tests for metrics module."""

from app.metrics import (
  grabs_total,
  last_success_timestamp_seconds,
  request_duration_seconds,
  request_errors_total,
  requests_total,
  run_total,
  skips_total,
  state_write_failures_total,
)


class TestMetrics:
  def test_metrics_are_defined(self) -> None:
    assert run_total is not None
    assert requests_total is not None
    assert grabs_total is not None
    assert skips_total is not None
    assert request_errors_total is not None
    assert request_duration_seconds is not None
    assert last_success_timestamp_seconds is not None
    assert state_write_failures_total is not None

  def test_metrics_have_labels(self) -> None:
    run_total.labels(target="test", type="radarr", status="success").inc()
    assert run_total.labels(target="test", type="radarr", status="success")._value.get() == 1.0

  def test_counter_increment(self) -> None:
    # Use unique target to avoid collision with arr_client tests that use target="test"
    requests_total.labels(target="test-metrics", type="radarr", operation="get_movies").inc()
    requests_total.labels(target="test-metrics", type="radarr", operation="get_movies").inc()
    assert (
      requests_total.labels(
        target="test-metrics", type="radarr", operation="get_movies"
      )._value.get()
      == 2.0
    )

  def test_gauge_set(self) -> None:
    last_success_timestamp_seconds.labels(target="test", type="radarr").set(1234.0)
    assert (
      last_success_timestamp_seconds.labels(target="test", type="radarr")._value.get() == 1234.0
    )

  def test_histogram_observe(self) -> None:
    request_duration_seconds.labels(target="test", type="radarr").observe(1.5)
    metric = request_duration_seconds.labels(target="test", type="radarr")
    assert metric._sum.get() == 1.5
