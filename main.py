import argparse
import logging
import sys

from models.project import Project
from models.user import User
from utils.display import (console, print_error, print_success, show_projects,
                           show_tasks, show_users)
from utils.helpers import get_project, get_user
from utils.storage import DEFAULT_DATA_FILE, load_users, save_users



def cmd_add_user(args, users):
    """Create a new user."""
    from utils.helpers import find_user
    if find_user(users, args.name):
        raise ValueError(f"User '{args.name}' already exists.")
    user = User(args.name, args.email)
    users.append(user)
    logging.info("Added user %s", user.name)
    print_success(f"User '{user.name}' added.")
    return True


def cmd_list_users(args, users):
    """Show all users."""
    show_users(users)
    return False


def cmd_add_project(args, users):
    """Add a project to a user."""
    user = get_user(users, args.user)
    project = user.add_project(Project(args.title, args.description, args.due))
    logging.info("Added project %s to %s", project.title, user.name)
    print_success(f"Project '{project.title}' added to {user.name}.")
    return True


def cmd_list_projects(args, users):
    """Show all projects, or only the projects of one user."""
    if args.user:
        user = get_user(users, args.user)
        show_projects(user.projects, title=f"Projects for {user.name}")
    else:
        all_projects = [p for user in users for p in user.projects]
        show_projects(all_projects)
    return False


def cmd_search_projects(args, users):
    """Search projects by keyword and/or user."""
    if not args.keyword and not args.user:
        raise ValueError("Give --keyword and/or --user to search.")
    results = []
    for user in users:
        if args.user and user.name.lower() != args.user.strip().lower():
            continue
        for project in user.projects:
            text = (project.title + " " + project.description).lower()
            if not args.keyword or args.keyword.lower() in text:
                results.append(project)
    show_projects(results, title="Search results")
    return False


def cmd_edit_project(args, users):
    """Change a project's title, description or due date."""
    if args.title is None and args.description is None and args.due is None:
        raise ValueError("Nothing to change. Use --title, --description or --due.")
    project = get_project(users, args.project, args.user)
    if args.title is not None:
        project.title = args.title
    if args.description is not None:
        project.description = args.description
    if args.due is not None:
        project.due_date = args.due
    logging.info("Edited project %s", project.title)
    print_success(f"Project '{project.title}' updated.")
    return True


def cmd_add_task(args, users):
    """Add a task to a project, optionally assigned to a user."""
    project = get_project(users, args.project, args.user)
    assigned = ""
    if args.assigned_to:
        assigned = get_user(users, args.assigned_to).name
    task = project.add_task(args.title, assigned)
    logging.info("Added task %s to %s", task.title, project.title)
    print_success(f"Task '{task.title}' added to '{project.title}'.")
    return True


def cmd_list_tasks(args, users):
    """Show the tasks of a project."""
    project = get_project(users, args.project, args.user)
    show_tasks(project)
    return False


def cmd_update_task(args, users):
    """Change a task's status or who it is assigned to."""
    if args.status is None and args.assigned_to is None:
        raise ValueError("Nothing to change. Use --status or --assigned-to.")
    project = get_project(users, args.project, args.user)
    task = project.find_task(args.task)
    if task is None:
        raise ValueError(f"Task '{args.task}' was not found in '{project.title}'.")
    if args.status is not None:
        task.status = args.status
    if args.assigned_to is not None:
        task.assigned_to = get_user(users, args.assigned_to).name
    print_success(f"Task '{task.title}' updated.")
    return True


def cmd_complete_task(args, users):
    """Mark a task as done."""
    project = get_project(users, args.project, args.user)
    task = project.find_task(args.task)
    if task is None:
        raise ValueError(f"Task '{args.task}' was not found in '{project.title}'.")
    task.complete()
    logging.info("Completed task %s", task.title)
    print_success(f"Task '{task.title}' marked as done.")
    return True


def add_user_option(parser):
    """Add the optional --user flag (only needed if two projects share a title)."""
    parser.add_argument("--user", help="project owner (only needed if titles clash)")


def build_parser():
    """Create the argparse parser with all the subcommands."""
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool - manage users, projects and tasks."
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True, help="user's name")
    p.add_argument("--email", default="", help="user's email (optional)")
    p.set_defaults(func=cmd_add_user)

    p = sub.add_parser("list-users", help="list all users")
    p.set_defaults(func=cmd_list_users)

    p = sub.add_parser("add-project", help="add a project to a user")
    p.add_argument("--user", required=True, help="owner's name")
    p.add_argument("--title", required=True, help="project title")
    p.add_argument("--description", default="", help="project description")
    p.add_argument("--due", default="", help="due date, e.g. 2026-12-01")
    p.set_defaults(func=cmd_add_project)

    p = sub.add_parser("list-projects", help="list projects (all or one user's)")
    p.add_argument("--user", help="only show this user's projects")
    p.set_defaults(func=cmd_list_projects)

    p = sub.add_parser("search-projects", help="search projects by keyword/user")
    p.add_argument("--keyword", help="word to look for in title/description")
    p.add_argument("--user", help="only search this user's projects")
    p.set_defaults(func=cmd_search_projects)

    p = sub.add_parser("edit-project", help="edit a project")
    p.add_argument("--project", required=True, help="current project title")
    add_user_option(p)
    p.add_argument("--title", help="new title")
    p.add_argument("--description", help="new description")
    p.add_argument("--due", help="new due date")
    p.set_defaults(func=cmd_edit_project)

    p = sub.add_parser("add-task", help="add a task to a project")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--title", required=True, help="task title")
    p.add_argument("--assigned-to", help="name of the user doing the task")
    add_user_option(p)
    p.set_defaults(func=cmd_add_task)

    p = sub.add_parser("list-tasks", help="list tasks in a project")
    p.add_argument("--project", required=True, help="project title")
    add_user_option(p)
    p.set_defaults(func=cmd_list_tasks)

    p = sub.add_parser("update-task", help="change a task's status or assignee")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--task", required=True, help="task title or ID")
    p.add_argument("--status", help="pending, in-progress or done")
    p.add_argument("--assigned-to", help="name of the user doing the task")
    add_user_option(p)
    p.set_defaults(func=cmd_update_task)

    p = sub.add_parser("complete-task", help="mark a task as done")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--task", required=True, help="task title or ID")
    add_user_option(p)
    p.set_defaults(func=cmd_complete_task)

    return parser


def main(argv=None, data_file=DEFAULT_DATA_FILE):
    """Run the CLI. Returns 0 on success and 1 on a user error."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:  
        parser.print_help()
        return 0

    users = load_users(data_file)
    try:
        changed = args.func(args, users)
    except ValueError as error:  
        logging.warning("Command failed: %s", error)
        print_error(f"Error: {error}")
        return 1

    if changed:
        save_users(users, data_file)
    return 0


if __name__ == "__main__":
    logging.basicConfig(filename="app.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    sys.exit(main())