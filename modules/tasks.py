from pathlib import Path
import json
from typing import List, Dict

TASKS_FILE = Path("tasks.json")


def load_tasks() -> List[Dict]:
    """
    Load tasks from the JSON file.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: List[Dict]) -> None:
    """
    Save tasks to the JSON file.
    """
    try:
        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

    except OSError as error:
        print(f"[SAVE ERROR] {error}")


def add_task(task_name: str) -> str:
    """
    Add a new task to the task list.
    """
    task_name = task_name.strip()

    if not task_name:
        return "Task name cannot be empty."

    tasks = load_tasks()

    tasks.append({
        "task": task_name,
        "status": "pending"
    })

    save_tasks(tasks)

    return f"Added '{task_name}' to your task list."


def view_tasks() -> str:
    """
    Return all tasks in a formatted string.
    """
    tasks = load_tasks()

    if not tasks:
        return "Your task list is currently empty."

    lines = ["Here are your tasks:\n"]

    for index, task in enumerate(tasks, start=1):
        lines.append(
            f"{index}. {task['task']} [{task['status']}]"
        )

    return "\n".join(lines)


def complete_task(task_index: int) -> str:
    """
    Mark a task as completed.
    """
    tasks = load_tasks()

    if not 1 <= task_index <= len(tasks):
        return "Invalid task number."

    tasks[task_index - 1]["status"] = "completed"

    save_tasks(tasks)

    return f"Task {task_index} marked as completed."


def delete_task(task_index: int) -> str:
    """
    Delete a task from the list.
    """
    tasks = load_tasks()

    if not 1 <= task_index <= len(tasks):
        return "Invalid task number."

    removed_task = tasks.pop(task_index - 1)

    save_tasks(tasks)

    return f"Deleted task: '{removed_task['task']}'"
