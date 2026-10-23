"""User: a Person who owns projects."""

from models.person import Person
from models.project import Project


class User(Person):
    """A user who has many projects (one-to-many)."""

    next_id = 1  

    def __init__(self, name, email="", user_id=None):
        """Create a user. Name and email are handled by Person."""
        super().__init__(name, email)
        self.projects = []
        if user_id is None:
            self.id = User.next_id
            User.next_id += 1
        else:
            self.id = user_id
            User.next_id = max(User.next_id, user_id + 1)

    def add_project(self, project):
        """Add a project to this user and set the project's owner."""
        if self.find_project(project.title):
            raise ValueError(f"{self.name} already has a project called '{project.title}'.")
        project.owner = self.name
        self.projects.append(project)
        return project

    def find_project(self, title):
        """Find one of this user's projects by title. Returns None if missing."""
        for project in self.projects:
            if project.title.lower() == str(title).strip().lower():
                return project
        return None

    def to_dict(self):
        """Turn the user (with projects and tasks) into a dictionary for JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        """Build a User (with projects and tasks) from a dictionary."""
        user = cls(data["name"], data.get("email", ""), data["id"])
        for project_data in data.get("projects", []):
            user.add_project(Project.from_dict(project_data))
        return user

    def __str__(self):
        """Readable text for printing."""
        return f"{self.name} ({len(self.projects)} projects)"

    def __repr__(self):
        """Text that helps when debugging."""
        return f"User(id={self.id}, name={self.name!r})"
    