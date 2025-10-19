# utils/storage.py
import json
from pathlib import  Path
from typing import List, Optional
from models.task import Task, Priority


STORAGE_FILE = Path("data/tasks.json")


def load_tasks() -> List[Task]:
    """
    Loads all tasks from the JSON storage file.
    Returns a list of validated task objects.
    If the file does not exist, an empty list is returned.
    """

    if not STORAGE_FILE.exists():
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        try:
            raw_tasks = json.load(f)
            # Convert list of dicts into Pydantic Task objects
            return [Task(**task) for task in raw_tasks]
        except json.JSONDecodeError:
            # Handles malformed JSON files gracefully
            return []


def save_tasks(tasks: List[Task]) -> None:
    """
    Saves a list of tasks to the JSON storage file.
    Uses Pydantic's .model_dump() for v2 compatibility.
    """
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    serializable_tasks = []
    for task in tasks:
        d = task.model_dump()
        # Convert datetimes to strings for safe JSON writing
        if isinstance(d.get("created_at"), object):
            d["created_at"] = task.created_at.strftime("%Y-%m-%d %H:%M")
        if d.get("due_date"):
            d["due_date"] = task.due_date.strftime("%Y-%m-%d")
        serializable_tasks.append(d)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_tasks, f, indent=4, ensure_ascii=False)


def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Retrieves a single task by its ID.
    Returns None if there is no such task.
    """

    for task in load_tasks():
        if task.id == task_id:
            return task
    return None


def get_next_task_id() -> int:
    """
    Determines the next unique task ID by finding
    the current highest ID and adding 1.
    Returns 1 if there are no tasks yet.
    """

    tasks = load_tasks()
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1