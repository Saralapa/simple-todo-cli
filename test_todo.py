import importlib
import json

import todo


def test_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Comprar pão")
    todo.list_tasks()

    out = capsys.readouterr().out
    assert "Comprar pão" in out


def test_mark_done_and_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Lavar louça")
    todo.mark_done(1)
    tasks = todo.load_tasks()
    assert tasks[0]["done"] is True

    todo.remove_task(1)
    assert todo.load_tasks() == []
