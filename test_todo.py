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


def test_edit_task(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Lavar carro")
    todo.edit_task(1, "Lavar moto")
    tasks = todo.load_tasks()
    assert tasks[0]["description"] == "Lavar moto"


def test_clear_tasks(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa 1")
    todo.add_task("Tarefa 2")
    todo.clear_tasks()
    assert todo.load_tasks() == []


def test_search_tasks(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Comprar leite")
    todo.add_task("Estudar Python")
    todo.search_tasks("python")

    out = capsys.readouterr().out
    assert "Estudar Python" in out
    assert "Comprar leite" not in out
