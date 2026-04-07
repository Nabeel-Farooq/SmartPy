import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(task_name):
    tasks = load_tasks()
    tasks.append({"task": task_name, "status": "pending"})
    save_tasks(tasks)
    return f"Added '{task_name}' to your task list."

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        return "Your task list is currently empty."
    
    response = "Here are your tasks:\n"
    for i, t in enumerate(tasks, 1):
        response += f"  {i}. {t['task']} [{t['status']}]\n"
    return response.strip()