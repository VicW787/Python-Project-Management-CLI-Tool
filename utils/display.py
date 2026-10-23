"""Pretty printing of tables and messages using the 'rich' package."""

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from utils.helpers import days_until

console = Console()


def print_success(message):
    """Print a green success message."""
    console.print(f"[green]{escape(message)}[/green]")


def print_error(message):
    """Print a red error message."""
    console.print(f"[red]{escape(message)}[/red]")


def due_label(due_date):
    """Return the due date with how many days are left, e.g. '2026-12-01 (44 days left)'."""
    if not due_date:
        return "-"
    days = days_until(due_date)
    if days < 0:
        return f"{due_date} (overdue)"
    return f"{due_date} ({days} days left)"


def show_users(users):
    """Print a table of users."""
    if not users:
        console.print("No users yet. Add one with: add-user --name NAME")
        return
    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")
    for user in users:
        table.add_row(str(user.id), escape(user.name), escape(user.email or "-"),
                      str(len(user.projects)))
    console.print(table)


def show_projects(projects, title="Projects"):
    """Print a table of projects."""
    if not projects:
        console.print("No projects found.")
        return
    table = Table(title=title)
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due")
    table.add_column("Tasks")
    table.add_column("Progress")
    for project in projects:
        table.add_row(str(project.id), escape(project.title), escape(project.owner),
                      due_label(project.due_date), str(len(project.tasks)),
                      f"{project.progress}%")
    console.print(table)


def show_tasks(project):
    """Print a table of the tasks in one project."""
    if not project.tasks:
        console.print(f"'{project.title}' has no tasks yet.")
        return
    table = Table(title=f"Tasks in {project.title}")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Assigned to")
    for task in project.tasks:
        colour = {"done": "green", "in-progress": "yellow"}.get(task.status, "white")
        table.add_row(str(task.id), escape(task.title),
                      f"[{colour}]{task.status}[/{colour}]",
                      escape(task.assigned_to or "-"))
    console.print(table)
    