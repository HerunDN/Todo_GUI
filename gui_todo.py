#!/usr/bin/env python3
import json
import os
import tkinter as tk
from tkinter import messagebox

FILE = os.path.join(os.path.dirname(__file__), 'todo.json')

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

class TodoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('To-Do List (GUI)')
        self.geometry('600x400')

        # Top frame: add task
        top = tk.Frame(self)
        top.pack(fill='x', padx=8, pady=6)

        tk.Label(top, text='Description:').pack(side='left')
        self.desc_entry = tk.Entry(top, width=40)
        self.desc_entry.pack(side='left', padx=6)

        tk.Label(top, text='Priority:').pack(side='left')
        self.priority_var = tk.StringVar(value='Medium')
        tk.OptionMenu(top, self.priority_var, 'High', 'Medium', 'Low').pack(side='left')

        tk.Button(top, text='Add', command=self.add_task).pack(side='left', padx=6)

        # Middle frame: list and scrollbar
        mid = tk.Frame(self)
        mid.pack(fill='both', expand=True, padx=8, pady=6)

        self.listbox = tk.Listbox(mid, activestyle='none')
        self.listbox.pack(side='left', fill='both', expand=True)
        sb = tk.Scrollbar(mid, command=self.listbox.yview)
        sb.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=sb.set)

        # Bottom frame: actions
        bot = tk.Frame(self)
        bot.pack(fill='x', padx=8, pady=6)

        tk.Button(bot, text='Mark Complete', command=self.complete_task).pack(side='left')
        tk.Button(bot, text='Delete', command=self.delete_task).pack(side='left', padx=6)

        tk.Label(bot, text='Search:').pack(side='left', padx=(10,0))
        self.search_entry = tk.Entry(bot, width=20)
        self.search_entry.pack(side='left', padx=6)
        tk.Button(bot, text='Find', command=self.search_tasks).pack(side='left')
        tk.Button(bot, text='Show All', command=self.refresh_list).pack(side='left', padx=6)

        self.refresh_list()

    def format_task(self, i, t):
        status = '✔' if t.get('completed') else ' '
        priority = t.get('priority', 'Medium')
        return f"{i}. [{status}] ({priority}) {t.get('description')}"

    def refresh_list(self, tasks=None):
        if tasks is None:
            tasks = load_tasks()
        self.listbox.delete(0, tk.END)
        for i, t in enumerate(tasks, start=1):
            self.listbox.insert(tk.END, self.format_task(i, t))

    def add_task(self):
        desc = self.desc_entry.get().strip()
        pr = self.priority_var.get() or 'Medium'
        if not desc:
            messagebox.showinfo('Add task', 'Description cannot be empty.')
            return
        tasks = load_tasks()
        tasks.append({'description': desc, 'completed': False, 'priority': pr})
        save_tasks(tasks)
        self.desc_entry.delete(0, tk.END)
        self.refresh_list()

    def complete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo('Complete', 'Select a task first.')
            return
        idx = sel[0]
        tasks = load_tasks()
        if 0 <= idx < len(tasks):
            tasks[idx]['completed'] = True
            save_tasks(tasks)
            self.refresh_list()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo('Delete', 'Select a task first.')
            return
        idx = sel[0]
        tasks = load_tasks()
        if 0 <= idx < len(tasks):
            confirm = messagebox.askyesno('Delete', f"Delete: {tasks[idx].get('description')}?")
            if confirm:
                tasks.pop(idx)
                save_tasks(tasks)
                self.refresh_list()

    def search_tasks(self):
        kw = self.search_entry.get().strip().lower()
        if not kw:
            messagebox.showinfo('Search', 'Enter a search keyword.')
            return
        tasks = load_tasks()
        matches = [t for t in tasks if kw in t.get('description', '').lower()]
        if not matches:
            messagebox.showinfo('Search', 'No matching tasks.')
            return
        self.refresh_list(tasks=matches)

if __name__ == '__main__':
    app = TodoGUI()
    app.mainloop()
