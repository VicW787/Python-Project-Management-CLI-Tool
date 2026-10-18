## Project Management CLI Tool

A command-line tool (Python) for managing users, projects and tasks. Data is saved in a JSON file so it is still there next time you run the tool.


### Features
1) Create and list users
2) Add projects to a user, list them, search them, edit them
3) Add tasks to projects, assign them to users, update status, mark complete
4) Progress % per project and "days left" until the due date
5) Data saved to data/data.json (missing/broken files are handled)
Colourful tables using the rich package

### Relationships: 
User to many Projects to many Tasks. A task can be assigned to any user, so users can contribute to projects they don't own. User inherits from Person.

### Debugging 
Actions are logged to app.log (ignored by git) — open it to trace what happened.