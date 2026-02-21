from __future__ import annotations

import argparse

from .storage import add_task, load_tasks, mark_done


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="test_project", description="Мини CLI: задачи")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Добавить задачу")
    p_add.add_argument("title", help="Текст задачи")

    sub.add_parser("list", help="Показать задачи")

    p_done = sub.add_parser("done", help="Отметить задачу выполненной")
    p_done.add_argument("id", type=int, help="ID задачи")

    return p


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "add":
        task = add_task(args.title)
        print(f"✅ Добавлено: [{task.id}] {task.title}")
        return 0

    if args.cmd == "list":
        tasks = load_tasks()
        if not tasks:
            print("Пока пусто.")
            return 0
        for t in tasks:
            flag = "✅" if t.done else "⏳"
            print(f"{flag} [{t.id}] {t.title}")
        return 0

    if args.cmd == "done":
        task = mark_done(args.id)
        if task is None:
            print("Не найдено.")
            return 1
        print(f"✅ Готово: [{task.id}] {task.title}")
        return 0

    return 2
