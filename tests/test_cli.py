"""Tests for the CLI commands (using a temporary data file)."""

import pytest

from main import main
from utils.storage import load_users


def run(tmp_path, *argv):
    """Helper: run the CLI against a temp file and return the exit code."""
    return main(list(argv), data_file=str(tmp_path / "data.json"))


def test_full_workflow(tmp_path):
    assert run(tmp_path, "add-user", "--name", "Alex") == 0
    assert run(tmp_path, "add-project", "--user", "Alex", "--title", "CLI Tool") == 0
    assert run(tmp_path, "add-task", "--project", "CLI Tool", "--title", "Do it",
               "--assigned-to", "Alex") == 0
    assert run(tmp_path, "complete-task", "--project", "CLI Tool", "--task", "Do it") == 0

    users = load_users(str(tmp_path / "data.json"))
    assert users[0].projects[0].tasks[0].status == "done"


def test_duplicate_user_fails(tmp_path):
    run(tmp_path, "add-user", "--name", "Alex")
    assert run(tmp_path, "add-user", "--name", "alex") == 1


def test_project_for_missing_user_fails(tmp_path):
    assert run(tmp_path, "add-project", "--user", "Ghost", "--title", "X") == 1


def test_bad_date_fails(tmp_path):
    run(tmp_path, "add-user", "--name", "Alex")
    assert run(tmp_path, "add-project", "--user", "Alex", "--title", "X",
               "--due", "banana") == 1


def test_task_for_missing_project_fails(tmp_path):
    assert run(tmp_path, "add-task", "--project", "Nope", "--title", "T") == 1


def test_search_and_list(tmp_path, capsys):
    run(tmp_path, "add-user", "--name", "Alex")
    run(tmp_path, "add-project", "--user", "Alex", "--title", "Website")
    capsys.readouterr()  
    assert run(tmp_path, "search-projects", "--keyword", "web") == 0
    assert "Website" in capsys.readouterr().out
    assert run(tmp_path, "list-projects", "--user", "Alex") == 0


def test_edit_project(tmp_path):
    run(tmp_path, "add-user", "--name", "Alex")
    run(tmp_path, "add-project", "--user", "Alex", "--title", "Old")
    assert run(tmp_path, "edit-project", "--project", "Old", "--title", "New") == 0
    users = load_users(str(tmp_path / "data.json"))
    assert users[0].projects[0].title == "New"


def test_missing_required_argument_exits(tmp_path):
    with pytest.raises(SystemExit):
        run(tmp_path, "add-user")  
