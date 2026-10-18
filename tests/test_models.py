"""Unit tests for the model classes."""

import pytest

from models.project import Project
from models.task import Task
from models.user import User


def test_user_is_a_person_with_validation():
    user = User("Alex", "alex@example.com")
    assert user.name == "Alex"
    with pytest.raises(ValueError):
        User("")
    with pytest.raises(ValueError):
        User("Sam", "not-an-email")


def test_ids_increase():
    first = Task("One")
    second = Task("Two")
    assert second.id == first.id + 1


def test_task_status_rules():
    task = Task("Write code")
    assert task.status == "pending"
    task.complete()
    assert task.status == "done"
    with pytest.raises(ValueError):
        task.status = "finished"


def test_project_date_validation():
    assert Project("A", due_date="1 Dec 2026").due_date == "2026-12-01"
    with pytest.raises(ValueError):
        Project("A", due_date="not a date")


def test_user_project_relationship():
    user = User("Alex")
    project = user.add_project(Project("CLI Tool"))
    assert project.owner == "Alex"
    assert user.find_project("cli tool") is project
    with pytest.raises(ValueError):
        user.add_project(Project("CLI Tool"))  


def test_project_tasks_progress_and_contributors():
    project = Project("CLI Tool")
    project.add_task("Task 1", "Alex")
    project.add_task("Task 2", "Sam")
    assert project.progress == 0
    project.find_task("Task 1").complete()
    assert project.progress == 50
    assert project.contributors == ["Alex", "Sam"]
    assert project.find_task(project.tasks[1].id) is project.tasks[1]
    with pytest.raises(ValueError):
        project.add_task("task 1") 