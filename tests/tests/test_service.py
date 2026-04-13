from pathlib import Path

import pytest

from test_project.service import complete_task, create_task, get_tasks


@pytest.fixture
def temp_db(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def test_create_task_strips_spaces(temp_db: Path) -> None:
    task = create_task("   hello   ", db_path=temp_db)

    assert task.title == "hello"


def test_create_task_empty_title_raises(temp_db: Path) -> None:
    with pytest.raises(ValueError):
        create_task("   ", db_path=temp_db)


def test_get_tasks_returns_created_tasks(temp_db: Path) -> None:
    create_task("first", db_path=temp_db)
    create_task("second", db_path=temp_db)

    tasks = get_tasks(db_path=temp_db)

    assert len(tasks) == 2
    assert tasks[0].title == "first"
    assert tasks[1].title == "second"


def test_complete_task_marks_done(temp_db: Path) -> None:
    task = create_task("demo", db_path=temp_db)

    done_task = complete_task(task.id, db_path=temp_db)

    assert done_task is not None
    assert done_task.done is True


def test_complete_task_invalid_id_raises(temp_db: Path) -> None:
    with pytest.raises(ValueError):
        complete_task(0, db_path=temp_db)
