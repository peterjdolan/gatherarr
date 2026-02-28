"""Tests for state management module."""

import tempfile
from pathlib import Path

import yaml

from app.state import (
  FileStateStorage,
  InMemoryStateStorage,
  ItemState,
  ItemStatus,
  RunStatus,
  StateManager,
  TargetState,
)


class TestStateManagerSerialization:
  """Tests for state serialization and deserialization to/from disk."""

  def test_save_and_load_serialization(self) -> None:
    """Test that state can be serialized to disk and deserialized."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)

      target_state = manager.get_target_state("test-target")
      target_state.last_run_timestamp = 1000.0
      target_state.last_success_timestamp = 999.0
      target_state.last_status = RunStatus.SUCCESS
      target_state.consecutive_failures = 0

      item_state = ItemState(
        item_id="123",
        last_processed_timestamp=500.0,
        last_result="search_triggered",
        last_status=ItemStatus.SUCCESS,
        consecutive_failures=0,
      )
      target_state.items["123"] = item_state

      manager.state.total_runs = 5
      manager.save()

      # Verify file was written
      assert state_path.exists()
      data = yaml.safe_load(state_path.read_text())
      assert data["total_runs"] == 5
      assert "test-target" in data["targets"]
      assert data["targets"]["test-target"]["last_run_timestamp"] == 1000.0

      # Load into new manager
      storage2 = FileStateStorage(state_path)
      manager2 = StateManager(storage2)
      manager2.load()

      assert manager2.state.total_runs == 5
      assert "test-target" in manager2.state.targets
      loaded_target = manager2.state.targets["test-target"]
      assert loaded_target.last_run_timestamp == 1000.0
      assert loaded_target.last_success_timestamp == 999.0
      assert loaded_target.last_status == RunStatus.SUCCESS
      assert "123" in loaded_target.items
      assert loaded_target.items["123"].item_id == "123"
      assert loaded_target.items["123"].last_status == ItemStatus.SUCCESS

  def test_load_nonexistent_file(self) -> None:
    """Test loading when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "nonexistent.yaml"
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)
      manager.load()
      assert manager.state.total_runs == 0

  def test_load_corrupted_file(self) -> None:
    """Test recovery from corrupted state file."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      state_path.write_text("invalid: yaml: content: [unclosed")

      storage = FileStateStorage(state_path)
      manager = StateManager(storage)
      manager.load()

      assert manager.state.total_runs == 0
      corrupt_files = list(state_path.parent.glob(".corrupt.*"))
      assert len(corrupt_files) == 1

  def test_load_missing_fields(self) -> None:
    """Test loading state with missing fields uses defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      state_path.write_text("{}")

      storage = FileStateStorage(state_path)
      manager = StateManager(storage)
      manager.load()

      assert manager.state.total_runs == 0
      assert len(manager.state.targets) == 0

  def test_atomic_write(self) -> None:
    """Test atomic write semantics."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)

      manager.state.total_runs = 1
      manager.save()

      assert state_path.exists()
      data = yaml.safe_load(state_path.read_text())
      assert data["total_runs"] == 1

  def test_load_state_with_consecutive_failures(self) -> None:
    """Test that consecutive_failures is serialized and deserialized correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      state_path.write_text(
        """total_runs: 1
targets:
  test-target:
    last_run_timestamp: 1000.0
    last_success_timestamp: 999.0
    last_status: success
    consecutive_failures: 0
    items:
      "42":
        item_id: "42"
        last_processed_timestamp: 500.0
        last_result: search_failed
        last_status: error
        consecutive_failures: 3
"""
      )
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)
      manager.load()

      target_state = manager.state.targets["test-target"]
      assert "42" in target_state.items
      assert target_state.items["42"].consecutive_failures == 3
      assert target_state.items["42"].last_status == ItemStatus.ERROR

  def test_load_state_without_consecutive_failures_uses_default(self) -> None:
    """Test backward compatibility: old state without consecutive_failures defaults to 0."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      state_path.write_text(
        """total_runs: 1
targets:
  test-target:
    last_run_timestamp: 1000.0
    last_success_timestamp: 999.0
    last_status: success
    consecutive_failures: 0
    items:
      "42":
        item_id: "42"
        last_processed_timestamp: 500.0
        last_result: search_failed
        last_status: error
"""
      )
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)
      manager.load()

      target_state = manager.state.targets["test-target"]
      assert target_state.items["42"].consecutive_failures == 0

  def test_multiple_targets_serialization(self) -> None:
    """Test serialization with multiple targets."""
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      storage = FileStateStorage(state_path)
      manager = StateManager(storage)

      target1 = manager.get_target_state("target1")
      target1.last_run_timestamp = 100.0

      target2 = manager.get_target_state("target2")
      target2.last_run_timestamp = 200.0

      manager.save()
      manager.load()

      assert len(manager.state.targets) == 2
      assert manager.state.targets["target1"].last_run_timestamp == 100.0
      assert manager.state.targets["target2"].last_run_timestamp == 200.0


class TestStateManager:
  """Tests for StateManager with disk I/O disabled."""

  def test_initial_state(self) -> None:
    """Test initial state is empty."""
    storage = InMemoryStateStorage()
    manager = StateManager(storage)
    assert manager.state.total_runs == 0
    assert len(manager.state.targets) == 0

  def test_get_target_state_creates_new(self) -> None:
    """Test get_target_state creates new target state."""
    storage = InMemoryStateStorage()
    manager = StateManager(storage)

    target_state = manager.get_target_state("new-target")
    assert isinstance(target_state, TargetState)
    assert target_state.last_run_timestamp == 0.0

  def test_state_persistence_in_memory(self) -> None:
    """Test that state persists in memory without disk I/O."""
    storage = InMemoryStateStorage()
    manager = StateManager(storage)

    target_state = manager.get_target_state("test-target")
    target_state.last_run_timestamp = 1000.0
    target_state.last_success_timestamp = 999.0
    target_state.last_status = RunStatus.SUCCESS
    target_state.consecutive_failures = 0

    item_state = ItemState(
      item_id="123",
      last_processed_timestamp=500.0,
      last_result="search_triggered",
      last_status=ItemStatus.SUCCESS,
      consecutive_failures=0,
    )
    target_state.items["123"] = item_state

    manager.state.total_runs = 5
    manager.save()  # Should be no-op with disk I/O disabled

    # State should still be in memory
    assert manager.state.total_runs == 5
    assert "test-target" in manager.state.targets
    assert manager.state.targets["test-target"].last_run_timestamp == 1000.0
    assert "123" in manager.state.targets["test-target"].items

  def test_multiple_targets_in_memory(self) -> None:
    """Test multiple targets work without disk I/O."""
    storage = InMemoryStateStorage()
    manager = StateManager(storage)

    target1 = manager.get_target_state("target1")
    target1.last_run_timestamp = 100.0

    target2 = manager.get_target_state("target2")
    target2.last_run_timestamp = 200.0

    assert len(manager.state.targets) == 2
    assert manager.state.targets["target1"].last_run_timestamp == 100.0
    assert manager.state.targets["target2"].last_run_timestamp == 200.0
