"""Project: belongs to one user and has many tasks."""

from models.task import Task
from utils.helpers import validate_date


class Project:
    """A project with a title, description, due date and a list of tasks."""

    next_id = 1  

    def __init__(self, title, description="", due_date="", owner="", project_id=None):
        """Create a project. owner is the name of the user who owns it."""
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner
        self.tasks = [] 
        if project_id is None:
            self.id = Project.next_id
            Project.next_id += 1
        else:
            self.id = project_id
            Project.next_id = max(Project.next_id, project_id + 1)

    @property
    def title(self):
        """Return the title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title. It cannot be empty."""
        value = str(value).strip()
        if not value:
            raise ValueError("Project title cannot be empty.")
        self._title = value

    @property
    def due_date(self):
        """Return the due date as YYYY-MM-DD (or empty text)."""
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        """Set the due date. validate_date makes sure it is a real date."""
        self._due_date = validate_date(value)

    @property
    def contributors(self):
        """Return the names of everyone who has a task in this project."""
        names = {task.assigned_to for task in self.tasks if task.assigned_to}
        return sorted(names)

    @property
    def progress(self):
        """Return the percentage of tasks that are done (0 if no tasks)."""
        if not self.tasks:
            return 0
        done = len([task for task in self.tasks if task.status == "done"])
        return int(done / len(self.tasks) * 100)

    def add_task(self, title, assigned_to=""):
        """Create a task and add it to this project."""
        if self.find_task(title):
            raise ValueError(f"Task '{title}' already exists in '{self.title}'.")
        task = Task(title, assigned_to=assigned_to)
        self.tasks.append(task)
        return task

    def find_task(self, identifier):
        """Find a task by its ID number or by its title. Returns None if missing."""
        identifier = str(identifier).strip()
        for task in self.tasks:
            if identifier.isdigit() and task.id == int(identifier):
                return task
            if task.title.lower() == identifier.lower():
                return task
        return None

    def to_dict(self):
        """Turn the project (and its tasks) into a dictionary for JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Project (and its tasks) from a dictionary."""
        project = cls(
            data["title"],
            data.get("description", ""),
            data.get("due_date", ""),
            project_id=data["id"],
        )
        for task_data in data.get("tasks", []):
            project.tasks.append(Task.from_dict(task_data))
        return project

    def __str__(self):
        """Readable text for printing."""
        return f"{self.title} ({len(self.tasks)} tasks, {self.progress}% done)"

    def __repr__(self):
        """Text that helps when debugging."""
        return f"Project(id={self.id}, title={self.title!r}, owner={self.owner!r})"
    