"""State management with atomic writes and recovery."""

import os
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Protocol

import yaml


class RunStatus(StrEnum):
  """Status of a run."""

  UNKNOWN = "unknown"
  SUCCESS = "success"
  ERROR = "error"


@dataclass
class ItemState:
  """State for a single processed item."""

  item_id: str
  last_processed_timestamp: float
  last_result: str
  last_status: str


@dataclass
class TargetState:
  """State for a single target."""

  last_run_timestamp: float = 0.0
  last_success_timestamp: float = 0.0
  last_status: RunStatus = RunStatus.UNKNOWN
  consecutive_failures: int = 0
  last_error_summary: str = ""
  items: dict[str, ItemState] = field(default_factory=dict)


@dataclass
class State:
  """Application state."""

  process_start_timestamp: float = field(default_factory=time.time)
  total_runs: int = 0
  targets: dict[str, TargetState] = field(default_factory=dict)


class StateStorage(Protocol):
  """Protocol for state storage operations."""

  def read(self) -> dict | None:
    """Read state data. Returns None if state doesn't exist."""
    ...

  def write(self, data: dict) -> None:
    """Write state data atomically."""
    ...


class FileStateStorage:
  """File-based state storage with atomic writes."""

  def __init__(self, state_file_path: Path | str) -> None:
    self.state_file_path = Path(state_file_path)

  def read(self) -> dict | None:
    """Read state from file."""
    if not self.state_file_path.exists():
      return None

    try:
      with open(self.state_file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
      return data if data is not None else {}
    except yaml.YAMLError:
      # Raise YAML errors to indicate corruption, caller will handle it
      raise

  def write(self, data: dict) -> None:
    """Write state to file using atomic write semantics."""
    self.state_file_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = self.state_file_path.with_suffix(f".tmp.{int(time.time())}")
    try:
      with open(temp_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
        f.flush()
        os.fsync(f.fileno())

      temp_path.replace(self.state_file_path)
      try:
        os.fsync(self.state_file_path.parent.open("r").fileno())
      except (OSError, AttributeError):
        pass
    finally:
      if temp_path.exists():
        try:
          temp_path.unlink()
        except OSError:
          pass

  def move_corrupted(self) -> None:
    """Move corrupted state file aside."""
    if not self.state_file_path.exists():
      return
    timestamp = int(time.time())
    corrupt_path = self.state_file_path.parent / f".corrupt.{timestamp}"
    try:
      self.state_file_path.rename(corrupt_path)
    except OSError:
      pass


class InMemoryStateStorage:
  """In-memory state storage for testing."""

  def __init__(self) -> None:
    self._data: dict | None = None

  def read(self) -> dict | None:
    """Read state from memory."""
    return self._data

  def write(self, data: dict) -> None:
    """Write state to memory."""
    self._data = data

  def move_corrupted(self) -> None:
    """No-op for in-memory storage."""
    pass


class StateManager:
  """Manages application state with atomic writes."""

  def __init__(self, storage: StateStorage) -> None:
    self.storage = storage
    self.state = State()

  def load(self) -> None:
    """Load state from storage, recovering from corruption if needed."""
    try:
      data = self.storage.read()
      if data is None:
        return

      try:
        self.state = self._deserialize(data)
      except (KeyError, ValueError, TypeError) as e:
        self._handle_corrupted_state(e)
    except yaml.YAMLError as e:
      # YAML parsing error indicates corruption
      self._handle_corrupted_state(e)

  def _deserialize(self, data: dict) -> State:
    """Deserialize state from dictionary."""
    state = State(
      process_start_timestamp=data.get("process_start_timestamp", time.time()),
      total_runs=data.get("total_runs", 0),
    )

    targets_data = data.get("targets", {})
    for target_name, target_data in targets_data.items():
      last_status_str = target_data.get("last_status", "unknown")
      try:
        last_status = RunStatus(last_status_str)
      except ValueError:
        last_status = RunStatus.UNKNOWN

      target_state = TargetState(
        last_run_timestamp=target_data.get("last_run_timestamp", 0.0),
        last_success_timestamp=target_data.get("last_success_timestamp", 0.0),
        last_status=last_status,
        consecutive_failures=target_data.get("consecutive_failures", 0),
        last_error_summary=target_data.get("last_error_summary", ""),
      )

      items_data = target_data.get("items", {})
      for item_id, item_data in items_data.items():
        target_state.items[item_id] = ItemState(
          item_id=item_data["item_id"],
          last_processed_timestamp=item_data["last_processed_timestamp"],
          last_result=item_data["last_result"],
          last_status=item_data["last_status"],
        )

      state.targets[target_name] = target_state

    return state

  def _handle_corrupted_state(self, error: Exception) -> None:
    """Handle corrupted state by moving it aside and starting fresh."""
    if hasattr(self.storage, "move_corrupted"):
      self.storage.move_corrupted()
    self.state = State()

  def save(self) -> None:
    """Save state to storage using atomic write semantics."""
    data = self._serialize()
    self.storage.write(data)

  def _serialize(self) -> dict:
    """Serialize state to dictionary using dataclasses.asdict."""
    data = asdict(self.state)
    # Convert RunStatus enum to string for YAML serialization
    for target_name, target_data in data.get("targets", {}).items():
      if "last_status" in target_data:
        status = target_data["last_status"]
        if isinstance(status, RunStatus):
          target_data["last_status"] = status.value
    return data

  def get_target_state(self, target_name: str) -> TargetState:
    """Get or create state for a target."""
    if target_name not in self.state.targets:
      self.state.targets[target_name] = TargetState()
    return self.state.targets[target_name]
