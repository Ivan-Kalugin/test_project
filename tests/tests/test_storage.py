from pathlib import Path

import pytest

from test_project.storage import add_task, load_tasks, mark_done


@pytest.fixture()
def temp_db(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def test_add_task_creates_task(temp_db: Path) -> None:
    add_task("Test task", db_path=temp_db)

    tasks = load_tasks(db_path=temp_db)

    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert not tasks[0].done


def test_mark_done_changes_status(temp_db: Path) -> None:
    task = add_task("Test task", db_path=temp_db)

    mark_done(task.id, db_path=temp_db)

    tasks = load_tasks(db_path=temp_db)

    assert tasks[0].done is True


def test_mark_done_nonexistent_returns_none(temp_db: Path) -> None:
    result = mark_done(999, db_path=temp_db)

    assert result is None
