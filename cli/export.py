# cli/export.py
"""
Export commands for the To-Do CLI App.

Provides commands to export tasks into Markdown, CSV, or JSON formats.
"""

from __future__ import annotations
import click
from rich.console import Console

from utils.storage import load_tasks
from utils.exporters import export_to_markdown, export_to_csv, export_to_json


console = Console()


@click.group()
def export():
    """Export tasks to various formats (Markdown, CSV, JSON)."""
    pass


# -------------------------------------------------------------------
# MARKDOWN EXPORT
# -------------------------------------------------------------------
@export.command("md")
@click.option("--filename", type=str, default="tasks.md", show_default=True, help="Name of the Markdown file.")
def export_md(filename: str):
    """Export tasks as a Markdown file."""
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]⚠ No tasks available to export.[/yellow]")
        return

    path = export_to_markdown(tasks, filename)
    console.print(f"✅ [green]Exported tasks to Markdown:[/green] {path}")


# -------------------------------------------------------------------
# CSV EXPORT
# -------------------------------------------------------------------
@export.command("csv")
@click.option("--filename", type=str, default="tasks.csv", show_default=True, help="Name of the CSV file.")
def export_csv(filename: str):
    """Export tasks as a CSV file."""
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]⚠ No tasks available to export.[/yellow]")
        return

    path = export_to_csv(tasks, filename)
    console.print(f"✅ [green]Exported tasks to CSV:[/green] {path}")


# -------------------------------------------------------------------
# JSON EXPORT
# -------------------------------------------------------------------
@export.command("json")
@click.option("--filename", type=str, default="tasks.json", show_default=True, help="Name of the JSON file.")
def export_json(filename: str):
    """Export tasks as a JSON file."""
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]⚠ No tasks available to export.[/yellow]")
        return

    path = export_to_json(tasks, filename)
    console.print(f"✅ [green]Exported tasks to JSON:[/green] {path}")