#utils/filters.py
from __future__ import annotations
from datetime import datetime, date
from typing import List, Optional
from models.task import Task


def filter_by_priority(tasks: List[Task], priority: Optional[str]) -> List[Task]:
    """
    Return tasks that match a given priority ("low", "medium", "high").
    If priority is None, return all tasks.
    """

    if not priority:
        return tasks

    priority = priority.lower()

    return [t for t in tasks if t.priority == priority]


def filter_by_tag(tasks: List[Task], tag: Optional[str]) -> List[Task]:
    """
    Returns tasks containing a specific tag.
    Tags are compared case-insensitive.
    """

    if not tag:
        return tasks
    tag = tag.lower()
    return [t for t in tasks if any(tag == tg.lower() for tg in t.tags)]


def filter_by_due_before(tasks: List[Task], due_before: Optional[date]) -> List[Task]:
    """
    Return tasks whose due_date is before the given date (not including the cutoff).
    """
    if not due_before:
        return tasks

    results = []
    for t in tasks:
        if not t.due_date:
            continue
        due_date = t.due_date.date() if isinstance(t.due_date, datetime) else t.due_date
        # Strictly before the cutoff date
        if due_date < due_before:
            results.append(t)
    return results


def filter_tasks(
        tasks: List[Task],
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        due_before: Optional[date] = None,
) -> List[Task]:
    """
    Apply all available filters to a list of tasks.
    You can mix filters (e.g. high-priority tasks due before 2025-12-01).
    """

    filtered = filter_by_priority(tasks, priority)
    filtered = filter_by_tag(filtered, tag)
    filtered = filter_by_due_before(filtered, due_before)
    return filtered