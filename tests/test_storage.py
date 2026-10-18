"""Unit tests for saving and loading JSON."""

from models.project import Project
from models.user import User
from utils.storage import load_users, save_users


def test_save_and_load_round_trip(tmp_path):
    path = str(tmp_path / "data.json")
    user = User("Alex", "alex@example.com")
    project = user.add_project(Project("CLI Tool", "A tool", "2026-12-01"))
    project.add_task("Task 1", "Alex").complete()

    assert save_users([user], path) is True
    loaded = load_users(path)

    assert loaded[0].name == "Alex"
    assert loaded[0].projects[0].due_date == "2026-12-01"
    assert loaded[0].projects[0].tasks[0].status == "done"


def test_missing_file_gives_empty_list(tmp_path):
    assert load_users(str(tmp_path / "nothing.json")) == []


def test_broken_file_is_backed_up(tmp_path):
    path = tmp_path / "data.json"
    path.write_text("{ this is not json")
    assert load_users(str(path)) == []
    assert (tmp_path / "data.json.bak").exists()


def test_ids_continue_after_loading(tmp_path):
    path = str(tmp_path / "data.json")
    user = User("Alex")
    user.add_project(Project("P1"))
    save_users([user], path)
    loaded = load_users(path)
    new_project = loaded[0].add_project(Project("P2"))
    assert new_project.id == 2
    