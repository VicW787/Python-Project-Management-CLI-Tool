"""Small helper functions used by the models and the CLI."""

from datetime import date

from dateutil import parser as date_parser  


def validate_date(text):
    """Turn text like '2026-12-01' or '1 Dec 2026' into 'YYYY-MM-DD'.

    Returns empty text if nothing was given. Raises ValueError if bad.
    """
    text = str(text).strip()
    if not text:
        return ""
    try:
        parsed = date_parser.parse(text)
    except (ValueError, OverflowError):
        raise ValueError(f"Could not understand the date '{text}'. Try YYYY-MM-DD.")
    return parsed.date().isoformat()


def days_until(due_date):
    """Return how many days are left until due_date (negative = overdue)."""
    if not due_date:
        return None
    return (date.fromisoformat(due_date) - date.today()).days


def find_user(users, name):
    """Find a user by name (not case sensitive). Returns None if missing."""
    for user in users:
        if user.name.lower() == str(name).strip().lower():
            return user
    return None


def get_user(users, name):
    """Like find_user, but raises an error with a clear message if missing."""
    user = find_user(users, name)
    if user is None:
        raise ValueError(f"User '{name}' was not found. Add them with add-user first.")
    return user


def get_project(users, title, user_name=None):
    """Find a project by title. Use user_name if two users share a title."""
    matches = []
    for user in users:
        if user_name and user.name.lower() != user_name.strip().lower():
            continue
        project = user.find_project(title)
        if project:
            matches.append(project)
    if not matches:
        raise ValueError(f"Project '{title}' was not found.")
    if len(matches) > 1:
        raise ValueError(
            f"More than one project is called '{title}'. Add --user to choose."
        )
    return matches[0]