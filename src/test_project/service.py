from __future__ import annotations

from pathlib import Path

from test_project.storage import Task, add_task, load_tasks, mark_done


def create_task(title: str, db_path: Path | None = None) -> Task:
    clean_title = title.strip()

    if not clean_title:
        raise ValueError("Task title cannot be empty")

    return add_task(clean_title, db_path=db_path)


def get_tasks(db_path: Path | None = None) -> list[Task]:
    return load_tasks(db_path=db_path)


def complete_task(task_id: int, db_path: Path | None = None) -> Task | None:
    if task_id <= 0:
        raise ValueError("Task ID must be positive")

    return mark_done(task_id, db_path=db_path)
