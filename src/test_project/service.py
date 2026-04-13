from __future__ import annotations

from pathlib import Path

from test_project.storage import (
    Task,
    load_tasks,
    mark_done,
    save_tasks,
)
from test_project.storage import (
    add_task as storage_add_task,
)


def create_task(title: str, db_path: Path | None = None) -> Task:
    clean_title = title.strip()

    if not clean_title:
        raise ValueError("Task title cannot be empty")

    return storage_add_task(clean_title, db_path=db_path)


def get_tasks(db_path: Path | None = None) -> list[Task]:
    return load_tasks(db_path=db_path)


def complete_task(task_id: int, db_path: Path | None = None) -> Task | None:
    if task_id <= 0:
        raise ValueError("Task ID must be positive")

    return mark_done(task_id, db_path=db_path)


def delete_task(task_id: int, db_path: Path | None = None) -> bool:
    if task_id <= 0:
        raise ValueError("Task ID must be positive")

    tasks = load_tasks(db_path=db_path)
    filtered_tasks = [task for task in tasks if task.id != task_id]

    if len(filtered_tasks) == len(tasks):
        return False

    save_tasks(filtered_tasks, db_path=db_path)
    return True
