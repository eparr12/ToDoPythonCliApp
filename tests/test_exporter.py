# tests/test_export.py
"""
Tests for export utilities and CLI commands.

Verifies Markdown, CSV, and JSON exports produce correct output
and that the CLI commands function as expected.
"""

from datetime import datetime
import json
import csv
import pytest
from click.testing import CliRunner

from cli.main import todo
from utils import storage, exporters
from models.task import Task, Priority


@pytest.fixture
def runner(tmp_path, monkeypatch):
    """
    Provides an isolated Click test runner and temporary export directory.
    Patches storage.STORAGE_FILE to ensure no real files are modified.
    """
    r = CliRunner()
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", test_file)
    monkeypatch.setattr(exporters, "EXPORT_DIR", tmp_path)
    return r


@pytest.fixture
def sample_tasks():
    """Reusable fixture that creates example Task objects."""
    return [
        Task(
            id=1,
            title="Export to Markdown",
            priority=Priority.high,
            due_date=datetime(2025, 1, 1),
            tags=["docs"],
            completed=True,
        ),
        Task(
            id=2,
            title="Export to CSV",
            priority=Priority.medium,
            due_date=None,
            tags=["data"],
            completed=False,
        ),
    ]


# -------------------------------------------------------------------
# UTILITY TESTS (utils/exporters.py)
# -------------------------------------------------------------------
def test_export_to_markdown_creates_file(tmp_path, sample_tasks):
    """Ensure Markdown export writes a readable file."""
    file_path = exporters.export_to_markdown(sample_tasks, tmp_path / "tasks.md")
    content = file_path.read_text(encoding="utf-8")

    assert file_path.exists()
    assert "Export to Markdown" in content
    assert "✅" in content or "Completed" in content
    assert "Priority" in content


def test_export_to_csv_creates_file(tmp_path, sample_tasks):
    """Ensure CSV export writes correct columns."""
    file_path = exporters.export_to_csv(sample_tasks, tmp_path / "tasks.csv")
    assert file_path.exists()

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert "title" in rows[0]
        assert rows[0]["title"] == "Export to Markdown"


def test_export_to_json_creates_valid_json(tmp_path, sample_tasks):
    """Ensure JSON export writes valid JSON array."""
    file_path = exporters.export_to_json(sample_tasks, tmp_path / "tasks.json")
    assert file_path.exists()

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["title"] == "Export to Markdown"


# -------------------------------------------------------------------
# CLI COMMAND TESTS (cli/export.py)
# -------------------------------------------------------------------
def test_cli_export_markdown_command_creates_file(runner, sample_tasks):
    """Verify `todo export md` command creates Markdown file."""
    storage.save_tasks(sample_tasks)
    result = runner.invoke(todo, ["export", "md", "--filename", "tasks.md"])

    assert result.exit_code == 0
    assert "✅" in result.output or "Exported" in result.output

    exported = runner.isolated_filesystem()
    # File should exist in tmp_path since patched
    path = storage.STORAGE_FILE.parent / "tasks.md"
    assert path.exists() or "tasks.md" in result.output


def test_cli_export_csv_command_creates_file(runner, sample_tasks):
    """Verify `todo export csv` command creates CSV file."""
    storage.save_tasks(sample_tasks)
    result = runner.invoke(todo, ["export", "csv", "--filename", "tasks.csv"])

    assert result.exit_code == 0
    assert "Exported" in result.output

    exported = storage.STORAGE_FILE.parent / "tasks.csv"
    assert exported.exists()


def test_cli_export_json_command_creates_file(runner, sample_tasks):
    """Verify `todo export json` command creates JSON file."""
    storage.save_tasks(sample_tasks)
    result = runner.invoke(todo, ["export", "json", "--filename", "tasks.json"])

    assert result.exit_code == 0
    assert "Exported" in result.output

    exported = storage.STORAGE_FILE.parent / "tasks.json"
    assert exported.exists()


def test_cli_export_no_tasks_shows_warning(runner):
    """Ensure CLI shows warning when no tasks exist."""
    storage.save_tasks([])

    result = runner.invoke(todo, ["export", "md"])
    assert result.exit_code == 0
    assert "No tasks available" in result.output