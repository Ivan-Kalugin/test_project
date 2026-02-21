from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool = False


def _default_db_path() -> Path:
    # Файл будет лежать в корне проекта: D:\Work\test_project\tasks.json
    # storage.py находится в src/test_project/storage.py
    # parents[2] -> src/test_project -> src -> project_root
    return Path(__file__).resolve().parents[2] / "tasks.json"


def load_tasks(db_path: Path | None = None) -> list[Task]:
    path = db_path or _default_db_path()
    if not path.exists():
        return []

    data: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []

    tasks: list[Task] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            tasks.append(
                Task(
                    id=int(item["id"]),
                    title=str(item["title"]),
                    done=bool(item.get("done", False)),
                )
            )
        except Exception:
            continue
    return tasks


def save_tasks(tasks: list[Task], db_path: Path | None = None) -> None:
    path = db_path or _default_db_path()
    payload = [asdict(t) for t in tasks]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def add_task(title: str, db_path: Path | None = None) -> Task:
    tasks = load_tasks(db_path)
    next_id = max((t.id for t in tasks), default=0) + 1
    task = Task(id=next_id, title=title, done=False)
    save_tasks([*tasks, task], db_path)
    return task


def mark_done(task_id: int, db_path: Path | None = None) -> Task | None:
    tasks = load_tasks(db_path)
    updated: list[Task] = []
    result: Task | None = None

    for t in tasks:
        if t.id == task_id:
            result = Task(id=t.id, title=t.title, done=True)
            updated.append(result)
        else:
            updated.append(t)

    if result is None:
        return None

    save_tasks(updated, db_path)
    return result
