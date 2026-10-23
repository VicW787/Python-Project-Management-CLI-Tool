"""Saving and loading data with JSON files."""

import json
import os

from models.project import Project
from models.task import Task
from models.user import User
from utils.display import print_error


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_FILE = os.path.join(BASE_DIR, "data", "data.json")


def save_users(users, path=DEFAULT_DATA_FILE):
    """Save all users (with their projects and tasks) to a JSON file.

    Returns True if it worked, False if there was a file problem.
    """
    data = {"users": [user.to_dict() for user in users]}
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w") as file:
            json.dump(data, file, indent=2)
        return True
    except OSError as error:
        print_error(f"Could not save data: {error}")
        return False


def load_users(path=DEFAULT_DATA_FILE):
    """Load users from a JSON file and return them as a list of User objects.

    - Missing file: returns an empty list (first run).
    - Broken file: the bad file is renamed to .bak and we start empty.
    """
    
    User.next_id = 1
    Project.next_id = 1
    Task.next_id = 1

    try:
        with open(path, "r") as file:
            data = json.load(file)
        return [User.from_dict(item) for item in data["users"]]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print_error(f"{path} is damaged. Saving a copy as .bak and starting fresh.")
        try:
            os.replace(path, path + ".bak")
        except OSError:
            pass
        User.next_id = Project.next_id = Task.next_id = 1
        return []