# task_manager.py
import json
import os
import shutil
from datetime import datetime
from typing import List, Optional

TASKS_FILE = "tasks.json"
BACKUP_FILE = "tasks_backup.json"

class Task:
    def __init__(self, title: str, deadline: Optional[str] = None, 
                 priority: str = "Medium", status: str = "Pending", tags: Optional[List[str]] = None,
                 completion_date: Optional[str] = None):
        self.title = title
        self.deadline = deadline  # Expected format: "YYYY-MM-DD"
        self.priority = priority  # High / Medium / Low
        self.status = status      # Pending / Done
        self.tags = tags or []
        self.completion_date = completion_date  # Date when task was marked done

    def is_overdue(self) -> bool:
        if self.deadline and self.status == "Pending":
            try:
                deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d").date()
                return datetime.today().date() > deadline_date
            except ValueError:
                return False
        return False

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status,
            "tags": self.tags,
            "completion_date": self.completion_date
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            title=data.get("title", ""),
            deadline=data.get("deadline"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending"),
            tags=data.get("tags", []),
            completion_date=data.get("completion_date")
        )

# --------------------------
# JSON Storage Functions
# --------------------------

def load_tasks() -> List[Task]:
    """Load tasks from JSON file with error recovery"""
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
    except FileNotFoundError:
        # Create empty tasks file if it doesn't exist
        save_tasks([])
        return []
    except json.JSONDecodeError:
        print("Error: tasks.json is corrupted.")
        # Try to restore from backup
        if os.path.exists(BACKUP_FILE):
            try:
                print("Attempting to restore from backup...")
                shutil.copy(BACKUP_FILE, TASKS_FILE)
                with open(TASKS_FILE, "r") as f:
                    data = json.load(f)
                    print("Successfully restored from backup!")
                    return [Task.from_dict(item) for item in data]
            except:
                print("Backup restore failed. Starting with empty task list.")
                save_tasks([])
                return []
        else:
            print("No backup available. Starting fresh.")
            save_tasks([])
            return []
    except Exception as e:
        print(f"Unexpected error loading tasks: {e}")
        return []

def save_tasks(tasks: List[Task]):
    """Save tasks to JSON file with automatic backup"""
    try:
        # Create backup of existing file before saving
        if os.path.exists(TASKS_FILE):
            try:
                shutil.copy(TASKS_FILE, BACKUP_FILE)
            except:
                pass  # Backup failed but continue with save
        
        # Save tasks
        with open(TASKS_FILE, "w") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)
    except Exception as e:
        print(f"Error saving tasks: {e}")
        raise

# --------------------------
# Task Operations
# --------------------------

def add_task(tasks: List[Task], task: Task):
    tasks.append(task)
    save_tasks(tasks)

def delete_task(tasks: List[Task], task_index: int):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks(tasks)

def mark_task_done(tasks: List[Task], task_index: int):
    if 0 <= task_index < len(tasks):
        tasks[task_index].status = "Done"
        tasks[task_index].completion_date = datetime.today().strftime("%Y-%m-%d")
        save_tasks(tasks)

def edit_task(tasks: List[Task], task_index: int, new_task: Task):
    if 0 <= task_index < len(tasks):
        tasks[task_index] = new_task
        save_tasks(tasks)
