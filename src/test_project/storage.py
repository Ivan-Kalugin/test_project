from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = Path("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


def _resolve_path(db_path: Path | None) -> Path:
    return db_path if db_path is not None else DEFAULT_DB_PATH


def load_tasks(db_path: Path | None = None) -> list[Task]:
    path = _resolve_path(db_path)

    if not path.exists():
        return []

    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # если файл повреждён — не падаем
        return []

    tasks: list[Task] = []
    for item in raw:
        tasks.append(
            Task(
                id=item["id"],
                title=item["title"],
                done=item["done"],
            )
        )

    return tasks


def save_tasks(tasks: list[Task], db_path: Path | None = None) -> None:
    path = _resolve_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = [asdict(task) for task in tasks]

    # atomic write
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
    ) as tmp:
        json.dump(payload, tmp, ensure_ascii=False, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name

    os.replace(temp_name, path)


def add_task(title: str, db_path: Path | None = None) -> Task:
    tasks = load_tasks(db_path)

    next_id = 1
    if tasks:
        next_id = max(t.id for t in tasks) + 1

    task = Task(id=next_id, title=title, done=False)
    tasks.append(task)

    save_tasks(tasks, db_path)

    return task


def mark_done(task_id: int, db_path: Path | None = None) -> Task | None:
    tasks = load_tasks(db_path)

    updated: list[Task] = []
    result: Task | None = None

    for t in tasks:
        if t.id == task_id:
            updated_task = Task(id=t.id, title=t.title, done=True)
            updated.append(updated_task)
            result = updated_task
        else:
            updated.append(t)

    if result is None:
        return None

    save_tasks(updated, db_path)
    return result
