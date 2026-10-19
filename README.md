## Project Management CLI Tool

A command-line tool (Python) for managing users, projects and tasks. Data is saved in a JSON file so it is still there next time you run the tool.


### Features
1) Create and list users
2) It adds projects to a user, lists them, searches them and edits them.
3) It adds tasks to projects, assigns them to users, updates their status and marks them complete.
4) It shows each project's progress (%) and "days left" until the due date.
5) Data saved to data/data.json (missing/broken files are handled)
Colourful tables using the rich package

### Relationships(How the Data is Organized): 
User to many Projects to many Tasks. A task can be assigned to any user, so users can contribute to projects they don't own. User inherits from Person.

### Setup
This needs a Python 3.8 or newer and git.
1. Clone the repository.
2. Create and activate a virtual environment.

   >python3 -m venv venv
   >source venv/bin/activate

3.Install the packages.
>   pip install -r requirements.txt
4. Check that everything works
>   python -m pytest
You should see all tests passed.

### Debugging 
Actions are logged to app.log (ignored by git) — open it to trace what happened.

### More Notes
1) Names and titles are not case sensitive, and values with spaces need quotes.
2) A task can be chosen by its title or its ID number.
3) Task status must be pending, in-progress or done.
Dates are best written as YYYY-MM-DD.
4) If two users have a project with the same title, add --user NAME to say which one you mean.