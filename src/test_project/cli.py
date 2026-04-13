from __future__ import annotations

import argparse

from test_project.service import complete_task, create_task, delete_task, get_tasks
from test_project.storage import Task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Simple task manager",
    )

    subparsers = parser.add_subparsers(dest="cmd", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    subparsers.add_parser("list", help="Show all tasks")

    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "add":
        task = create_task(args.title)
        print(f"Added task #{task.id}: {task.title}")
        return 0

    if args.cmd == "list":
        tasks = get_tasks()

        if not tasks:
            print("No tasks yet.")
            return 0

        for task in tasks:
            status = "x" if task.done else " "
            print(f"[{status}] {task.id}: {task.title}")

        return 0

    if args.cmd == "done":
        done_task: Task | None = complete_task(args.id)

        if done_task is None:
            print("Task not found.")
            return 1

        print(f"Task #{done_task.id} marked as done.")
        return 0

    if args.cmd == "delete":
        deleted = delete_task(args.id)

        if not deleted:
            print("Task not found.")
            return 1

        print(f"Task #{args.id} deleted.")
        return 0

    return 2
