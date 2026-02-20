#!/usr/bin/env python3
"""Quick test to verify tasks are loading correctly"""
from task_manager import load_tasks

tasks = load_tasks()
print(f"Loaded {len(tasks)} tasks:")
for i, task in enumerate(tasks):
    print(f"{i+1}. {task.title} - {task.priority} - {task.status} - Deadline: {task.deadline}")
