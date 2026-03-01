"""Prometheus metrics collection."""

from prometheus_client import Counter, Gauge, Histogram

run_total = Counter(
  "gatherarr_run_total",
  "Total number of runs",
  ["target", "type", "status"],
)

requests_total = Counter(
  "gatherarr_requests_total",
  "Total number of API requests",
  ["target", "type", "operation"],
)

request_errors_total = Counter(
  "gatherarr_request_errors_total",
  "Total number of request errors",
  ["target", "type", "operation"],
)

grabs_total = Counter(
  "gatherarr_grabs_total",
  "Total number of items grabbed",
  ["target", "type"],
)

skips_total = Counter(
  "gatherarr_skips_total",
  "Total number of items skipped",
  ["target", "type"],
)

request_duration_seconds = Histogram(
  "gatherarr_request_duration_seconds",
  "Request duration in seconds",
  ["target", "type"],
  buckets=(0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0),
)

last_success_timestamp_seconds = Gauge(
  "gatherarr_last_success_timestamp_seconds",
  "Last successful run timestamp",
  ["target", "type"],
)

state_write_failures_total = Counter(
  "gatherarr_state_write_failures_total",
  "Total number of state write failures",
)
