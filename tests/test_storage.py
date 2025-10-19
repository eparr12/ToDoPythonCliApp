# tests/test_storage.py
"""
Tests for utils/storage.py
Verifies saving, loading, and ID generation for Task objects.
"""

from datetime import datetime
import pytest

from models.task import Task, Priority
from utils import storage


@pytest.fixture
def tmp_tasks_file(tmp_path, monkeypatch):
    """
    Creates a temporary storage file for testing and replaces
    utils.storage.STORAGE_FILE with this temporary file path.
    This ensures tests never touch the real tasks.json.
    """
    tmp_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", tmp_file)
    return tmp_file


def make_task(id_: int = 1) -> Task:
    """Helper to quickly create a Task object for testing."""
    return Task(
        id=id_,
        title=f"Task {id_}",
        priority=Priority.medium,
        due_date=datetime(2025, 1, 1),
        tags=["test"],
        completed=False,
    )


# -------------------------------------------------------------------
# SAVE AND LOAD
# -------------------------------------------------------------------
def test_save_and_load_tasks(tmp_tasks_file):
    """Ensure that tasks save and load correctly from JSON."""
    tasks = [make_task(1), make_task(2)]

    storage.save_tasks(tasks)
    assert tmp_tasks_file.exists(), "File should be created after saving."

    loaded = storage.load_tasks()
    assert len(loaded) == 2
    assert loaded[0].title == "Task 1"
    assert loaded[1].id == 2


# -------------------------------------------------------------------
# EMPTY FILE HANDLING
# -------------------------------------------------------------------
def test_load_tasks_handles_missing_file(tmp_path, monkeypatch):
    """Should return an empty list when the file doesn’t exist."""
    tmp_file = tmp_path / "no_file.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", tmp_file)

    result = storage.load_tasks()
    assert result == []


def test_load_tasks_handles_empty_file(tmp_tasks_file):
    """Should handle an empty JSON file gracefully."""
    tmp_tasks_file.write_text("[]", encoding="utf-8")
    result = storage.load_tasks()
    assert result == []


# -------------------------------------------------------------------
# NEXT TASK ID
# -------------------------------------------------------------------
def test_get_next_task_id_increments_correctly(tmp_tasks_file):
    """Verify ID increments from highest existing value."""
    tasks = [make_task(1), make_task(2), make_task(10)]
    storage.save_tasks(tasks)

    next_id = storage.get_next_task_id()
    assert next_id == 11


def test_get_next_task_id_when_empty(tmp_tasks_file):
    """Verify ID starts at 1 when no tasks exist."""
    storage.save_tasks([])
    next_id = storage.get_next_task_id()
    assert next_id == 1


# -------------------------------------------------------------------
# GET TASK BY ID
# -------------------------------------------------------------------
def test_get_task_by_id_returns_correct_task(tmp_tasks_file):
    """Ensure get_task_by_id finds the right task."""
    tasks = [make_task(1), make_task(2)]
    storage.save_tasks(tasks)

    found = storage.get_task_by_id(2)
    assert found is not None
    assert found.id == 2


def test_get_task_by_id_returns_none_if_missing(tmp_tasks_file):
    """Ensure get_task_by_id returns None for missing IDs."""
    storage.save_tasks([make_task(1)])
    assert storage.get_task_by_id(99) is None