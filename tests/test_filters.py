# tests/test_filters.py
"""
Tests for utils/filters.py

Verifies that filtering by priority, tag, and due date works correctly.
"""

from datetime import datetime, timedelta
from models.task import Task, Priority
from utils import filters


# -------------------------------------------------------------------
# HELPER: CREATE SAMPLE TASKS
# -------------------------------------------------------------------
def make_sample_tasks():
    """Create a small set of sample tasks for filtering tests."""
    today = datetime.now()
    return [
        Task(id=1, title="High Priority Work", priority=Priority.high, due_date=today, tags=["work"]),
        Task(id=2, title="Medium Study", priority=Priority.medium, due_date=today + timedelta(days=1), tags=["study"]),
        Task(id=3, title="Low Personal", priority=Priority.low, due_date=today + timedelta(days=7), tags=["personal"]),
        Task(id=4, title="High Urgent", priority=Priority.high, due_date=today - timedelta(days=1), tags=["urgent", "work"]),
    ]


# -------------------------------------------------------------------
# PRIORITY FILTERING
# -------------------------------------------------------------------
def test_filter_by_priority_high_only():
    """Ensure only high-priority tasks are returned."""
    tasks = make_sample_tasks()
    result = filters.filter_tasks(tasks, priority="high")
    assert all(t.priority == Priority.high for t in result)
    assert len(result) == 2  # two high-priority tasks


def test_filter_by_priority_medium_only():
    """Ensure only medium-priority tasks are returned."""
    tasks = make_sample_tasks()
    result = filters.filter_tasks(tasks, priority="medium")
    assert len(result) == 1
    assert result[0].title == "Medium Study"


# -------------------------------------------------------------------
# TAG FILTERING
# -------------------------------------------------------------------
def test_filter_by_tag_work():
    """Ensure tasks with 'work' tag are returned."""
    tasks = make_sample_tasks()
    result = filters.filter_tasks(tasks, tag="work")
    assert len(result) == 2
    assert all("work" in t.tags for t in result)


def test_filter_by_tag_personal():
    """Ensure tasks with 'personal' tag are returned."""
    tasks = make_sample_tasks()
    result = filters.filter_tasks(tasks, tag="personal")
    assert len(result) == 1
    assert result[0].title == "Low Personal"


# -------------------------------------------------------------------
# DUE DATE FILTERING
# -------------------------------------------------------------------
def test_filter_by_due_before_tomorrow():
    """Ensure tasks due before or on a certain date are returned."""
    tasks = make_sample_tasks()
    tomorrow = datetime.now().date() + timedelta(days=1)
    result = filters.filter_tasks(tasks, due_before=tomorrow)
    assert all(t.due_date.date() <= tomorrow for t in result)
    assert len(result) == 2  # one today, one yesterday


def test_filter_by_due_before_past_date():
    """No tasks should match when date is too early."""
    tasks = make_sample_tasks()
    cutoff = datetime.now().date() - timedelta(days=3)
    result = filters.filter_tasks(tasks, due_before=cutoff)
    assert result == []


# -------------------------------------------------------------------
# COMBINED FILTERS
# -------------------------------------------------------------------
def test_filter_by_priority_and_tag():
    """Ensure combining filters returns intersection of both criteria."""
    tasks = make_sample_tasks()
    result = filters.filter_tasks(tasks, priority="high", tag="urgent")
    assert len(result) == 1
    assert result[0].title == "High Urgent"