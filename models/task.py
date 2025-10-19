# models/task.py
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional,List
from pydantic import BaseModel, Field, field_validator
import json

class Priority(str, Enum):
    """
    Enum representing task priority levels.
    Inherits from both str and Enum so the value behaves like a string
    (for JSON serialization) while still being restricted to fixed options.
    """

    low = "low"
    medium = "medium"
    high = "high"


class Task(BaseModel):
    """
    Represents a single task in the to-do list.
    Uses Pydantic's BaseModel for automatic data validation and serialization.
    """

    id: int
    title: str = Field(...,min_length=1, max_length=255)
    priority: Priority = Priority.medium
    due_date: Optional[datetime] = None
    tags: List[str] = []
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


    @field_validator("tags", mode="before")
    @classmethod
    def ensure_tags_list(cls, v):
        """
        Ensures that tags is always a list.
        Converts None to empty list to prevent runtime errors when joining tags.
        """

        if v is None:
            return []
        return v


    def to_markdown(self) -> str:
        """
        Exports the task as a formatted markdown string.
        Includes icons for completion status, and displays priority, due date, and tags.
        """

        # Use emoji icons for polish
        status_icon = "✅" if self.completed else "❌"

        # Format due date if present, otherwise fallback string
        due = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No due date"

        # Join all tags into one comma-separated string, e.g. "work, urgent"
        tags_str = ", ".join(self.tags) if self.tags else "None"

        # Returns formatted Markdown
        return(
            f"- {status_icon} **{self.title}** "
            f"(Priority: {self.priority}, Due: {due}, Tags: {tags_str})"
        )


    def to_dict(self):
        """Convert Task to a serializable dictionary."""
        d = self.model_dump()
        # Format datetimes as strings for JSON/CSV
        if self.due_date:
            d["due_date"] = self.due_date.strftime("%Y-%m-%d")
        if self.created_at:
            d["created_at"] = self.created_at.strftime("%Y-%m-%d %H:%M")
        return d


    def to_json(self):
        """Return a JSON string representation of the task."""
        return json.dumps(self.to_dict(), indent=4)