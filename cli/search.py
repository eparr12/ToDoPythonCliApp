# cli/search.py
"""
Search and filter commands for the To-Do CLI App.

Allows filtering tasks by priority, tag, or due date.
"""

from __future__ import annotations
import click
from datetime import datetime
from rich.console import Console
from rich.table import Table

from utils.storage import load_tasks
from utils.filters import filter_tasks


console = Console()


@click.group()
def search():
    """Search or filter tasks."""
    pass


# -------------------------------------------------------------------
# FILTER COMMAND
# -------------------------------------------------------------------
@search.command("by")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    help="Filter tasks by priority level.",
)
@click.option("--tag", type=str, help="Filter tasks by a specific tag.")
@click.option(
    "--due-before",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Filter tasks due on or before this date (YYYY-MM-DD).",
)
def search_by(priority: str, tag: str, due_before: datetime):
    """
    Filter tasks by one or more criteria.

    Examples:
      todo search by --priority high
      todo search by --tag work
      todo search by --due-before 2025-12-01
    """
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]⚠ No tasks found to search.[/yellow]")
        return

    filtered = filter_tasks(
        tasks,
        priority=priority,
        tag=tag,
        due_before=due_before.date() if due_before else None,
    )

    if not filtered:
        console.print("[red]No matching tasks found.[/red]")
        return

    table = Table(title="🔍 Filtered Tasks", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Title", style="bold cyan")
    table.add_column("Priority", justify="center")
    table.add_column("Due", justify="center")
    table.add_column("Tags", style="magenta")
    table.add_column("Status", justify="center")

    for t in filtered:
        status = "✅" if t.completed else "❌"
        due = t.due_date.strftime("%Y-%m-%d") if t.due_date else "-"
        tags_str = ", ".join(t.tags) if t.tags else "-"
        table.add_row(str(t.id), t.title, t.priority.value, due, tags_str, status)

    console.print(table)
