# tests/test_cli_tasks.py
"""
Tests for cli/tasks.py

Verifies that Click commands work correctly: add, list, update, complete, delete.
"""

from datetime import datetime
import json
import pytest
from click.testing import CliRunner

from cli.main import todo
from utils import storage


@pytest.fixture
def runner(tmp_path, monkeypatch):
    """
    Provides an isolated Click test runner and patches the storage file
    so tests never modify real user data.
    """
    r = CliRunner()
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", test_file)
    return r


# -------------------------------------------------------------------
# ADD COMMAND
# -------------------------------------------------------------------
def test_add_task_creates_entry(runner):
    """Ensure adding a task stores it in the JSON file."""
    result = runner.invoke(
        todo, ["tasks", "add", "Write tests", "--priority", "high", "--tags", "dev"]
    )
    assert result.exit_code == 0
    assert "✅" in result.output or "Task added" in result.output

    tasks = storage.load_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Write tests"
    assert tasks[0].priority.name == "high"


# -------------------------------------------------------------------
# LIST COMMAND
# -------------------------------------------------------------------
def test_list_tasks_displays_table(runner):
    """Ensure list command prints a table of tasks."""
    # Preload a task
    t = storage.Task(
        id=1,
        title="Example Task",
        priority=storage.Priority.medium,
        due_date=datetime(2025, 1, 1),
        tags=["demo"],
    )
    storage.save_tasks([t])

    result = runner.invoke(todo, ["tasks", "list"])
    assert result.exit_code == 0
    assert "Example Task" in result.output
    assert "Priority" in result.output
    assert "❌" in result.output or "✅" in result.output


# -------------------------------------------------------------------
# COMPLETE COMMAND
# -------------------------------------------------------------------
def test_complete_marks_task_done(runner):
    """Ensure the complete command sets completed=True."""
    t = storage.Task(
        id=1,
        title="Complete me",
        priority=storage.Priority.low,
        due_date=None,
        tags=[],
    )
    storage.save_tasks([t])

    result = runner.invoke(todo, ["tasks", "complete", "1"])
    assert result.exit_code == 0
    assert "🎉" in result.output

    loaded = storage.load_tasks()
    assert loaded[0].completed is True


# -------------------------------------------------------------------
# UPDATE COMMAND
# -------------------------------------------------------------------
def test_update_task_changes_fields(runner):
    """Ensure the update command modifies task fields."""
    t = storage.Task(
        id=1,
        title="Old title",
        priority=storage.Priority.low,
        due_date=datetime(2025, 5, 1),
        tags=["old"],
    )
    storage.save_tasks([t])

    result = runner.invoke(
        todo,
        [
            "tasks",
            "update",
            "1",
            "--title",
            "New title",
            "--priority",
            "high",
            "--tags",
            "updated",
        ],
    )

    assert result.exit_code == 0
    assert "✏️" in result.output

    updated = storage.load_tasks()[0]
    assert updated.title == "New title"
    assert updated.priority == storage.Priority.high
    assert updated.tags == ["updated"]


# -------------------------------------------------------------------
# DELETE COMMAND
# -------------------------------------------------------------------
def test_delete_task_removes_entry(runner):
    """Ensure the delete command removes a task."""
    t = storage.Task(
        id=1,
        title="Delete me",
        priority=storage.Priority.medium,
        due_date=None,
        tags=[],
    )
    storage.save_tasks([t])

    result = runner.invoke(todo, ["tasks", "delete", "1"])
    assert result.exit_code == 0
    assert "🗑️" in result.output or "deleted" in result.output

    tasks = storage.load_tasks()
    assert tasks == []


# -------------------------------------------------------------------
# EDGE CASES
# -------------------------------------------------------------------
def test_complete_nonexistent_task_shows_error(runner):
    """Should display a clear error for missing task ID."""
    storage.save_tasks([])
    result = runner.invoke(todo, ["tasks", "complete", "99"])
    assert result.exit_code == 0
    assert "not found" in result.output.lower()


def test_delete_nonexistent_task_shows_error(runner):
    """Should display a clear error for deleting invalid ID."""
    storage.save_tasks([])
    result = runner.invoke(todo, ["tasks", "delete", "42"])
    assert result.exit_code == 0
    assert "not found" in result.output.lower()