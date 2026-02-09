# Simple To-Do List (CLI)

Usage:

1. Ensure you have Python 3.7+ installed.
2. Run the app:

```bash
python todo.py
```

Commands in the app:
- Add task: Enter a description to add a new task.
- View tasks: Lists tasks with their numbers and completion status.
- Mark task complete: Provide the task number to mark it completed.
- Delete task: Provide the task number to remove it.

New features:
- Task priority: When adding a task you can choose `High`, `Medium`, or `Low` (default `Medium`).
- Search: Use the in-app search option to find tasks by keyword in the description.

Persistent storage is in `todo.json` located next to `todo.py`.

GUI:

- A simple Tkinter GUI is available in `gui_todo.py`.
- Run the GUI with:

```bash
python gui_todo.py
```

The GUI supports add/list/mark-complete/delete/search and uses the same `todo.json` file.
