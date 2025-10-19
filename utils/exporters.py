# utils/exporters.py
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import List
from models.task import Task


EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_to_markdown(tasks: List[Task], filename: str = "tasks.md") -> Path:
    """
    Export tasks to Markdown file.
    Each task uses the Task.to_markdown() method for consistent formatting.
    Returns the path to the exported file.
    """

    filepath = EXPORT_DIR / filename
    with filepath.open("w", encoding="utf-8") as f:
        f.write("# 📝 To-Do List\n\n")
        if not tasks:
            f.write("_No tasks found._\n")
            return filepath
        for t in tasks:
            f.write(t.to_markdown() + "\n")
    return filepath


def export_to_csv(tasks: List[Task], filename: str = "tasks.csv") -> Path:
    """
    Export tasks to CSV file.
    Uses Python's build-in csv module for compatibility.
    """

    filepath = EXPORT_DIR / filename
    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "priority", "due_date", "tags", "completed", "created_at"])
        for t in tasks:
            writer.writerow([
                t.id,
                t.title,
                t.priority.value,
                t.due_date.strftime("Y-%m-%d") if t.due_date else "",
                ", ".join(t.tags),
                "✅" if t.completed else "❌",
                t.created_at.strftime("%Y-%m-%d %H:%M"),
            ])
    return filepath


def export_to_json(tasks, filepath):
    """
    Export tasks to a standalone JSON file.
    Useful for backups or machine-readable APIs.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)
    return filepath