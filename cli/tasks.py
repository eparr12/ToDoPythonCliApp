# cli/tasks.py
"""
Task management commands for the To-Do CLI App.

Handles adding, listing, updating, completing, and deleting tasks.
"""

from __future__ import annotations
import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

from models.task import Task, Priority
from utils.storage import load_tasks, save_tasks, get_next_task_id, get_task_by_id


console = Console()


@click.group()
def tasks():
    """Manage your tasks."""
    pass


# -------------------------------------------------------------------
# ADD
# -------------------------------------------------------------------
@tasks.command("add")
@click.argument("title")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    default="medium",
    show_default=True,
)
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), help="Due date (YYYY-MM-DD)")
@click.option("--tags", multiple=True, help="Add one or more tags, e.g. --tags work --tags coding")
def add_task(title: str, priority: str, due: datetime, tags: list[str]):
    """Add a new task."""
    tasks_list = load_tasks()
    new_task = Task(
        id=get_next_task_id(),
        title=title,
        priority=Priority(priority.lower()),
        due_date=due,
        tags=list(tags),
    )

    tasks_list.append(new_task)
    save_tasks(tasks_list)
    console.print(f"✅ [green]Task added:[/green] {new_task.title}")


# -------------------------------------------------------------------
# LIST
# -------------------------------------------------------------------
@tasks.command("list")
@click.option("--show-completed/--hide-completed", default=True, show_default=True)
def list_tasks(show_completed: bool):
    """List all tasks in a formatted table."""
    tasks_list = load_tasks()

    if not tasks_list:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="📋 To-Do List", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Title", style="bold cyan")
    table.add_column("Priority", justify="center")
    table.add_column("Due", justify="center")
    table.add_column("Tags", style="magenta")
    table.add_column("Status", justify="center")

    for t in tasks_list:
        if not show_completed and t.completed:
            continue
        status = "✅" if t.completed else "❌"
        due = t.due_date.strftime("%Y-%m-%d") if t.due_date else "-"
        table.add_row(str(t.id), t.title, t.priority.value, due, ", ".join(t.tags), status)

    console.print(table)


# -------------------------------------------------------------------
# COMPLETE
# -------------------------------------------------------------------
@tasks.command("complete")
@click.argument("task_id", type=int)
def complete_task(task_id: int):
    """Mark a task as completed."""
    tasks_list = load_tasks()
    task = get_task_by_id(task_id)

    if not task:
        console.print(f"[red]Task with ID {task_id} not found.[/red]")
        return

    for t in tasks_list:
        if t.id == task_id:
            t.completed = True
            break

    save_tasks(tasks_list)
    console.print(f"🎉 [green]Task {task_id} marked as complete![/green]")


# -------------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------------
@tasks.command("update")
@click.argument("task_id", type=int)
@click.option("--title", type=str, help="Update the task title.")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    help="Update priority level.",
)
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), help="Update due date (YYYY-MM-DD)")
@click.option("--tags", multiple=True, help="Replace tags completely.")
def update_task(task_id: int, title: str, priority: str, due: datetime, tags: list[str]):
    """Update an existing task."""
    tasks_list = load_tasks()
    task = get_task_by_id(task_id)

    if not task:
        console.print(f"[red]Task with ID {task_id} not found.[/red]")
        return

    for t in tasks_list:
        if t.id == task_id:
            if title:
                t.title = title
            if priority:
                t.priority = Priority(priority.lower())
            if due:
                t.due_date = due
            if tags:
                t.tags = list(tags)
            break

    save_tasks(tasks_list)
    console.print(f"✏️ [cyan]Task {task_id} updated.[/cyan]")


# -------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------
@tasks.command("delete")
@click.argument("task_id", type=int)
def delete_task(task_id: int):
    """Delete a task permanently."""
    tasks_list = load_tasks()
    updated_tasks = [t for t in tasks_list if t.id != task_id]

    if len(updated_tasks) == len(tasks_list):
        console.print(f"[red]Task with ID {task_id} not found.[/red]")
        return

    console.print("🗑️ Deleting task...")
    for _ in track(range(20), description="Removing..."):
        pass

    save_tasks(updated_tasks)
    console.print(f"[red]Task {task_id} deleted.[/red]")
