#!/usr/bin/env python3
import json
import os
import sys

FILE = os.path.join(os.path.dirname(__file__), 'todo.json')

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_tasks(tasks):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task(description, priority='Medium'):
    tasks = load_tasks()
    tasks.append({'description': description, 'completed': False, 'priority': priority})
    save_tasks(tasks)
    print('Task added.')

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('No tasks found.')
        return
    for i, t in enumerate(tasks, start=1):
        status = '✔' if t.get('completed') else ' '
        priority = t.get('priority', 'Medium')
        print(f"{i}. [{status}] ({priority}) {t.get('description')}")

def search_tasks(keyword):
    tasks = load_tasks()
    matches = []
    for i, t in enumerate(tasks, start=1):
        if keyword.lower() in t.get('description', '').lower():
            matches.append((i, t))
    if not matches:
        print('No matching tasks found.')
        return
    for i, t in matches:
        status = '✔' if t.get('completed') else ' '
        priority = t.get('priority', 'Medium')
        print(f"{i}. [{status}] ({priority}) {t.get('description')}")

def complete_task(index):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        tasks[index-1]['completed'] = True
        save_tasks(tasks)
        print('Task marked complete.')
    else:
        print('Invalid task number.')

def delete_task(index):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index-1)
        save_tasks(tasks)
        print(f"Deleted task: {removed.get('description')}")
    else:
        print('Invalid task number.')

def prompt_int(prompt_text):
    try:
        return int(input(prompt_text).strip())
    except Exception:
        return None

def main():
    while True:
        print('\nTo-Do List')
        print('1. Add task')
        print('2. View tasks')
        print('3. Mark task complete')
        print('4. Delete task')
        print('5. Search tasks')
        print('6. Exit')
        choice = input('Choose an option: ').strip()
        if choice == '1':
            desc = input('Task description: ').strip()
            if desc:
                # prompt for priority
                p = input('Priority (High/Medium/Low) [Medium]: ').strip().title()
                if p not in ('High', 'Medium', 'Low'):
                    p = 'Medium'
                add_task(desc, p)
            else:
                print('Empty description; task not added.')
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            list_tasks()
            idx = prompt_int('Enter task number to mark complete: ')
            if idx is not None:
                complete_task(idx)
            else:
                print('Invalid number.')
        elif choice == '4':
            list_tasks()
            idx = prompt_int('Enter task number to delete: ')
            if idx is not None:
                delete_task(idx)
            else:
                print('Invalid number.')
        elif choice == '5':
            keyword = input('Enter keyword to search for: ').strip()
            if keyword:
                search_tasks(keyword)
            else:
                print('Empty keyword.')
        elif choice == '6':
            print('Goodbye.')
            break
        else:
            print('Invalid choice. Please select 1-6.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')
