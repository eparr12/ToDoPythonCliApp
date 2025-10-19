# tests/test_task_model.py
"""
Tests for models/task.py

Verifies validation, default values, and serialization of the Task model.
"""

from datetime import datetime, date
import pytest
from pydantic import ValidationError

from models.task import Task, Priority


# -------------------------------------------------------------------
# BASIC CREATION
# -------------------------------------------------------------------
def test_create_valid_task():
    """Ensure a valid Task object can be created."""
    task = Task(
        id=1,
        title="Write documentation",
        priority=Priority.high,
        due_date=datetime(2025, 12, 1),
        tags=["docs", "writing"],
        completed=False,
    )

    assert task.id == 1
    assert task.title == "Write documentation"
    assert task.priority == Priority.high
    assert isinstance(task.due_date, datetime)
    assert "docs" in task.tags
    assert task.completed is False


# -------------------------------------------------------------------
# DEFAULT VALUES
# -------------------------------------------------------------------
def test_task_defaults_if_optional_fields_missing():
    """Ensure defaults are correctly applied when optional fields are not provided."""
    task = Task(id=2, title="Quick note")

    assert task.priority == Priority.medium
    assert task.completed is False
    assert task.due_date is None
    assert task.tags == []


# -------------------------------------------------------------------
# VALIDATION ERRORS
# -------------------------------------------------------------------
def test_invalid_priority_raises_validation_error():
    """Ensure invalid priority strings raise a ValidationError."""
    with pytest.raises(ValidationError):
        Task(id=3, title="Invalid priority test", priority="urgent")


def test_invalid_due_date_type_raises_error():
    """Ensure invalid due_date types raise a ValidationError."""
    with pytest.raises(ValidationError):
        Task(id=4, title="Invalid date", due_date="not-a-date")


def test_missing_required_fields_raise_error():
    """Ensure id and title are required fields."""
    with pytest.raises(ValidationError):
        Task(priority=Priority.low)  # Missing ID and title


# -------------------------------------------------------------------
# SERIALIZATION
# -------------------------------------------------------------------
def test_to_dict_and_to_json_methods():
    """Ensure Task serializes to a clean dict and JSON string."""
    task = Task(
        id=5,
        title="Serialize test",
        priority=Priority.low,
        due_date=datetime(2025, 6, 15),
        tags=["test"],
        completed=True,
    )

    d = task.to_dict()
    assert isinstance(d, dict)
    assert d["title"] == "Serialize test"
    assert "due_date" in d

    json_str = task.to_json()
    assert isinstance(json_str, str)
    assert '"Serialize test"' in json_str


# -------------------------------------------------------------------
# MARKDOWN EXPORT
# -------------------------------------------------------------------
def test_to_markdown_output():
    """Ensure Task exports correctly to Markdown format."""
    task = Task(
        id=6,
        title="Markdown example",
        priority=Priority.medium,
        due_date=datetime(2025, 3, 5),
        tags=["markdown", "test"],
        completed=True,
    )

    md = task.to_markdown()
    assert isinstance(md, str)
    assert "Markdown example" in md
    assert "✅" in md or "Completed" in md
    assert "Priority" in md