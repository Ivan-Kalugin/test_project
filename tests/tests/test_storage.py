from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = Path("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


def load_tasks(db_path: Path = DEFAULT_DB_PATH) -> list[Task]:
    path = Path(db_path)

    if not path.exists():
        return []

    data: Any = json.loads(path.read_text(encoding="utf-8"))

    tasks: list[Task] = []
    for item in data:
        tasks.append(
            Task(
                id=item["id"],
                title=item["title"],
                done=item["done"],
            )
        )

    return tasks


def save_tasks(tasks: list[Task], db_path: Path = DEFAULT_DB_PATH) -> None:
    path = Path(db_path)

    data = [asdict(task) for task in tasks]

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_task(title: str, db_path: Path = DEFAULT_DB_PATH) -> Task:
    tasks = load_tasks(db_path)

    next_id = 1
    if tasks:
        next_id = max(task.id for task in tasks) + 1

    task = Task(id=next_id, title=title, done=False)
    tasks.append(task)

    save_tasks(tasks, db_path)

    return task


def mark_done(task_id: int, db_path: Path = DEFAULT_DB_PATH) -> Task | None:
    tasks = load_tasks(db_path)

    for task in tasks:
        if task.id == task_id:
            task.done = True
            save_tasks(tasks, db_path)
            return task

    return None
