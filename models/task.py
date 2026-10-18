"""Task: one piece of work inside a project."""

VALID_STATUSES = ("pending", "in-progress", "done")


class Task:
    """A task with a title, a status and a person it is assigned to."""

    next_id = 1  

    def __init__(self, title, status="pending", assigned_to="", task_id=None):
        """Create a task. If task_id is given (loading from file) we keep it."""
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        if task_id is None:
            self.id = Task.next_id
            Task.next_id += 1
        else:
            self.id = task_id
            
            Task.next_id = max(Task.next_id, task_id + 1)

    @property
    def title(self):
        """Return the title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title. It cannot be empty."""
        value = str(value).strip()
        if not value:
            raise ValueError("Task title cannot be empty.")
        self._title = value

    @property
    def status(self):
        """Return the status."""
        return self._status

    @status.setter
    def status(self, value):
        """Set the status. Must be pending, in-progress or done."""
        value = str(value).strip().lower()
        if value not in VALID_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(VALID_STATUSES)}."
            )
        self._status = value

    def complete(self):
        """Mark the task as done."""
        self.status = "done"

    def to_dict(self):
        """Turn the task into a dictionary so it can be saved as JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Task from a dictionary (used when loading from JSON)."""
        return cls(
            data["title"],
            data.get("status", "pending"),
            data.get("assigned_to", ""),
            data["id"],
        )

    def __str__(self):
        """Readable text for printing."""
        return f"[{self.status}] {self.title}"

    def __repr__(self):
        """Text that helps when debugging."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"