"""Tests for state management module."""

import tempfile
from pathlib import Path

import yaml

from app.state import (
  STATE_SIZE_CAP_BYTES,
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


class TestStateSizeCap:
  """Tests for state size cap pruning."""

  def test_no_pruning_when_under_cap(self) -> None:
    """State under cap is not pruned."""
    cap = 1024 * 1024  # 1 MB - plenty for a few items
    storage = InMemoryStateStorage()
    manager = StateManager(storage, state_size_cap_bytes=cap)

    target = manager.get_target_state("target1")
    for i in range(10):
      target.items[str(i)] = ItemState(
        item_id=str(i),
        last_processed_timestamp=1000.0 + i,
        last_result="ok",
        last_status=ItemStatus.SUCCESS,
      )

    manager.save()

    assert len(target.items) == 10

  def test_prunes_oldest_items_when_over_cap(self) -> None:
    """When state would exceed cap, oldest items (by last_processed_timestamp) are pruned."""
    cap = 400  # Small cap to force pruning with few items
    storage = InMemoryStateStorage()
    manager = StateManager(storage, state_size_cap_bytes=cap)

    target = manager.get_target_state("target1")
    target.items["old"] = ItemState(
      item_id="old",
      last_processed_timestamp=100.0,  # Oldest
      last_result="ok",
      last_status=ItemStatus.SUCCESS,
    )
    target.items["middle"] = ItemState(
      item_id="middle",
      last_processed_timestamp=200.0,
      last_result="ok",
      last_status=ItemStatus.SUCCESS,
    )
    target.items["new"] = ItemState(
      item_id="new",
      last_processed_timestamp=300.0,  # Newest
      last_result="ok",
      last_status=ItemStatus.SUCCESS,
    )

    manager.save()

    # Oldest should be pruned first; "old" may be pruned
    assert "new" in target.items
    assert "old" not in target.items

  def test_pruning_persists_to_file(self) -> None:
    """Pruned state is what gets written to disk."""
    cap = 400
    with tempfile.TemporaryDirectory() as tmpdir:
      state_path = Path(tmpdir) / "state.yaml"
      storage = FileStateStorage(state_path)
      manager = StateManager(storage, state_size_cap_bytes=cap)

      target = manager.get_target_state("target1")
      for i in range(20):
        target.items[str(i)] = ItemState(
          item_id=str(i),
          last_processed_timestamp=100.0 + i,  # Lower i = older
          last_result="ok",
          last_status=ItemStatus.SUCCESS,
        )

      manager.save()

      written = state_path.read_text()
      assert len(written.encode("utf-8")) <= cap
      data = yaml.safe_load(written)
      item_count = len(data["targets"]["target1"]["items"])
      assert item_count < 20

  def test_default_cap_is_10_mb(self) -> None:
    """Default state size cap is 10 MB."""
    storage = InMemoryStateStorage()
    manager = StateManager(storage)
    assert manager.state_size_cap_bytes == STATE_SIZE_CAP_BYTES
    assert STATE_SIZE_CAP_BYTES == 10 * 1024 * 1024
