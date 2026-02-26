"""State management with atomic writes and recovery."""

import os
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Protocol

import structlog
import yaml

logger = structlog.get_logger()


class RunStatus(StrEnum):
  """Status of a run."""

  UNKNOWN = "unknown"
  SUCCESS = "success"
  ERROR = "error"


class ItemStatus(StrEnum):
  """Status of an individual item processing attempt."""

  UNKNOWN = "unknown"
  SUCCESS = "success"
  ERROR = "error"


@dataclass
class ItemState:
  """State for a single processed item."""

  item_id: str
  last_processed_timestamp: float
  last_result: str
  last_status: ItemStatus

  def logging_ids(self) -> dict[str, str]:
    """Logging identifiers for the item."""
    return {
      "item_id": self.item_id,
      "item_last_processed_timestamp": str(self.last_processed_timestamp),
      "item_last_result": self.last_result,
      "item_last_status": self.last_status.value,
    }


@dataclass
class TargetState:
  """State for a single target."""

  last_run_timestamp: float = 0.0
  last_success_timestamp: float = 0.0
  last_status: RunStatus = RunStatus.UNKNOWN
  consecutive_failures: int = 0
  items: dict[str, ItemState] = field(default_factory=dict)

  def logging_ids(self) -> dict[str, str]:
    """Logging identifiers for the item."""
    return {
      "target_last_run_timestamp": str(self.last_run_timestamp),
      "target_last_success_timestamp": str(self.last_success_timestamp),
      "target_last_status": self.last_status.value,
      "target_consecutive_failures": str(self.consecutive_failures),
    }


@dataclass
class State:
  """Application state."""

  process_start_timestamp: float = field(default_factory=time.time)
  total_runs: int = 0
  targets: dict[str, TargetState] = field(default_factory=dict)

  def logging_ids(self) -> dict[str, str]:
    """Logging identifiers for the state."""
    return {
      "process_start_timestamp": str(self.process_start_timestamp),
      "total_runs": str(self.total_runs),
      "target_count": str(len(self.targets)),
    }


class StateStorage(Protocol):
  """Protocol for state storage operations."""

  def read(self) -> dict | None:
    """Read state data. Returns None if state doesn't exist."""
    ...

  def write(self, data: dict) -> None:
    """Write state data atomically."""
    ...

  def move_corrupted(self) -> None:
    """Move corrupted state aside (no-op for storage types that don't support it)."""
    ...


class FileStateStorage:
  """File-based state storage with atomic writes."""

  def __init__(self, state_file_path: Path | str) -> None:
    self.state_file_path = Path(state_file_path)

  def read(self) -> dict | None:
    """Read state from file."""
    logger.debug("Reading state from file", state_file_path=str(self.state_file_path))
    if not self.state_file_path.exists():
      logger.debug("State file does not exist", state_file_path=str(self.state_file_path))
      return None

    try:
      with open(self.state_file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
      result = data if data is not None else {}
      logger.debug(
        "State read successfully", state_file_path=str(self.state_file_path), has_data=bool(result)
      )
      return result
    except yaml.YAMLError as e:
      logger.warning(
        "YAML error while reading state", state_file_path=str(self.state_file_path), error=str(e)
      )
      # Raise YAML errors to indicate corruption, caller will handle it
      raise

  def write(self, data: dict) -> None:
    """Write state to file using atomic write semantics."""
    logger.debug("Writing state to file", state_file_path=str(self.state_file_path))
    self.state_file_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = self.state_file_path.with_suffix(f".tmp.{int(time.time())}")
    logger.debug(
      "Using temporary file for atomic write",
      temp_path=str(temp_path),
      state_file_path=str(self.state_file_path),
    )
    try:
      with open(temp_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
        f.flush()
        os.fsync(f.fileno())
      logger.debug("Temporary file written and synced", temp_path=str(temp_path))

      temp_path.replace(self.state_file_path)
      logger.debug(
        "Temporary file replaced state file",
        temp_path=str(temp_path),
        state_file_path=str(self.state_file_path),
      )
      try:
        with self.state_file_path.parent.open("r") as parent_fd:
          os.fsync(parent_fd.fileno())
      except OSError, AttributeError:
        pass
      logger.debug("State file written successfully", state_file_path=str(self.state_file_path))
    finally:
      if temp_path.exists():
        logger.debug("Cleaning up temporary file", temp_path=str(temp_path))
        try:
          temp_path.unlink()
        except OSError:
          pass

  def move_corrupted(self) -> None:
    """Move corrupted state file aside."""
    if not self.state_file_path.exists():
      logger.debug("No state file to move (corrupted)", state_file_path=str(self.state_file_path))
      return
    timestamp = int(time.time())
    corrupt_path = self.state_file_path.parent / f".corrupt.{timestamp}"
    logger.debug(
      "Moving corrupted state file",
      state_file_path=str(self.state_file_path),
      corrupt_path=str(corrupt_path),
    )
    try:
      self.state_file_path.rename(corrupt_path)
      logger.debug(
        "Corrupted state file moved",
        state_file_path=str(self.state_file_path),
        corrupt_path=str(corrupt_path),
      )
    except OSError as e:
      logger.error(
        "Failed to move corrupted state file",
        state_file_path=str(self.state_file_path),
        error=str(e),
      )
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
    logger.debug("Loading state from storage")
    try:
      data = self.storage.read()
      if data is None:
        logger.debug("No state data found, starting with fresh state")
        return

      logger.debug("Deserializing state data", has_data=bool(data))
      try:
        self.state = self._deserialize(data)
        logger.debug(
          "State loaded successfully",
          **self.state.logging_ids(),
        )
      except (KeyError, ValueError, TypeError) as e:
        logger.error("State deserialization failed", error=str(e))
        self._handle_corrupted_state(e)
    except yaml.YAMLError as e:
      logger.error("YAML parsing error while loading state", error=str(e))
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
      )

      items_data = target_data.get("items", {})
      for item_id, item_data in items_data.items():
        item_status_str = item_data.get("last_status", ItemStatus.UNKNOWN.value)
        try:
          item_status = ItemStatus(item_status_str)
        except ValueError:
          item_status = ItemStatus.UNKNOWN

        target_state.items[item_id] = ItemState(
          item_id=item_data["item_id"],
          last_processed_timestamp=item_data["last_processed_timestamp"],
          last_result=item_data["last_result"],
          last_status=item_status,
        )

      state.targets[target_name] = target_state

    return state

  def _handle_corrupted_state(self, error: Exception) -> None:
    """Handle corrupted state by moving it aside and starting fresh."""
    logger.warning("State corruption detected, resetting..", error=str(error))
    self.storage.move_corrupted()
    self.state = State()

  def save(self) -> None:
    """Save state to storage using atomic write semantics."""
    logger.debug(
      "Saving state",
      **self.state.logging_ids(),
    )
    data = self._serialize()
    logger.debug("State serialized, writing to storage")
    self.storage.write(data)
    logger.debug("State saved successfully")

  def _serialize(self) -> dict:
    """Serialize state to dictionary using dataclasses.asdict."""
    data = asdict(self.state)
    # Convert enum values to strings for YAML serialization
    for target_data in data.get("targets", {}).values():
      if "last_status" in target_data:
        status = target_data["last_status"]
        if isinstance(status, RunStatus):
          target_data["last_status"] = status.value
      for item_data in target_data.get("items", {}).values():
        item_status = item_data.get("last_status")
        if isinstance(item_status, ItemStatus):
          item_data["last_status"] = item_status.value
    return data

  def get_target_state(self, target_name: str) -> TargetState:
    """Get or create state for a target."""
    if target_name not in self.state.targets:
      logger.debug("Creating new target state", target=target_name)
      self.state.targets[target_name] = TargetState()
    else:
      logger.debug("Retrieving existing target state", target=target_name)
    return self.state.targets[target_name]
