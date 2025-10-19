# cli/main.py
"""
Main entry point for the To-Do CLI App

This file defines the root Click command group 'todo'
and registers subcommand groups from cli/tasks.py, cli/export.py, and cli/search.py
"""


from __future__ import annotations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import click

# import subcommand groups
from cli.tasks import tasks
from cli.export import export
from cli.search import search


@click.group(invoke_without_command=True)
@click.pass_context
def todo(ctx: click.Context):
    """
    📝 To-Do CLI App

    Manage your tasks directly from the command line:
    add, list, update, complete, delete, search, and export.

    Example usage:
        todo tasks add "Learn Python" --priority high --tags learning code
        todo export md
        todo search --tag work
    """


    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# -------------------------------------------------------------------
# Register the subcommand groups
# -------------------------------------------------------------------
todo.add_command(tasks) # type: ignore
todo.add_command(export) # type: ignore
todo.add_command(search) # type: ignore


def main():
    """Entry point for CLI execution"""
    todo()


if __name__ == "__main__":
    main()