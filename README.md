## Project Management CLI Tool

A command-line tool (Python) for managing users, projects and tasks. Data is saved in a JSON file so it is still there next time you run the tool.


### Features
1) Create and list users
2) It adds projects to a user, lists them, searches them and edits them.
3) It adds tasks to projects, assigns them to users, updates their status and marks them complete.
4) It shows each project's progress (%) and "days left" until the due date.
5) Data saved to data/data.json (missing/broken files are handled).
6) Clear tables and coloured messages using the rich package.
7) Helpful error messages instead of crashes

### Relationships(How the Data is Organized): 
User --> to many Projects --> to many Tasks. A task can be assigned to any user, so users can contribute to projects they don't own. 
User inherits from Person.

### Setup
This needs a Python 3.8 or newer and git.
1. Clone the repository.
2. Create and activate a virtual environment:

   >python3 -m venv venv
   >source venv/bin/activate

3.Install the packages.
>pip install -r requirements.txt

Using pipenv instead? Run:
 >pipenv istall --dev

and put 
 >pipenv run 

before each command below.

4.Check that everything works: 
>python -m pytest

You should see all tests passed.

## How to Run CLI Commands
General form: ``` python main.py <command> [options]```

```
python main.py --help
```

```
python main.py add-task --help
```

### Quick Walkthrough

```
python main.py add-user --name "Alex" --email alex@example.com
```

```
python main.py add-project --user "Alex" --title "CLI Tool" --description "My tool" --due 2026-12-15
```

```
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
```

```
python main.py list-tasks --project "CLI Tool"
```

```
python main.py complete-task --project "CLI Tool" --task "Implement add-task"
```

```
python main.py list-projects
```

### Command Reference

| Command | What it does | Example |
|---|---|---|
| `add-user` | Create a user | `python main.py add-user --name "Alex" --email alex@example.com` |
| `list-users` | Show all users | `python main.py list-users` |
| `add-project` | Add a project to a user | `python main.py add-project --user "Alex" --title "CLI Tool" --due 2026-12-15` |
| `list-projects` | Show all projects, or one user's | `python main.py list-projects --user "Alex"` |
| `search-projects` | Search by keyword and/or user | `python main.py search-projects --keyword tool` |
| `edit-project` | Change title, description or due date | `python main.py edit-project --project "CLI Tool" --due 2027-01-10` |
| `add-task` | Add a task to a project | `python main.py add-task --project "CLI Tool" --title "Write tests" --assigned-to "Alex"` |


### Debugging 
Actions are logged to app.log (ignored by git) — open it to trace what happened. 

### More Notes 
1) Names and titles are not case sensitive, and the values with spaces need quotes. 
2) A task can be chosen by its title or its ID number.
3) Task status must be ```pending```, ```in-progress``` or ```done```.
Dates are best written as ```YYYY-MM-DD```.
4) If two users have a project with the same title, add ```--user NAME``` to say which one you mean.
5) Actions are logged to ```app.log``` (ignored by git), which helps when debugging.

### How To Run The Tests
```
python -m pytest
```

```
python -m pytest -v
```

### A Few Issues
There are no delete commands. Users cannot be renamed, and user names must be unique.
