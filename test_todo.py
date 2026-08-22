import importlib
import json

import todo


def test_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Comprar pão")
    todo.list_tasks()

    out = capsys.readouterr().out
    assert "Comprar pão" in out


def test_add_task_with_due(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Pagar aluguel", due="2026-09-01")
    tasks = todo.load_tasks()
    assert tasks[0]["due"] == "2026-09-01"


def test_add_task_without_due(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa sem prazo")
    tasks = todo.load_tasks()
    assert "due" not in tasks[0]


def test_list_overdue(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa vencida", due="2020-01-01")
    todo.add_task("Tarefa futura", due="2099-01-01")
    capsys.readouterr()
    todo.list_overdue(today="2026-01-01")

    out = capsys.readouterr().out
    assert "Tarefa vencida" in out
    assert "Tarefa futura" not in out


def test_list_overdue_ignores_done(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa vencida concluída", due="2020-01-01")
    todo.mark_done(1)
    capsys.readouterr()
    todo.list_overdue(today="2026-01-01")

    out = capsys.readouterr().out
    assert "Nenhuma tarefa vencida." in out


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


def test_add_task_with_priority(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa urgente", priority="alta")
    tasks = todo.load_tasks()
    assert tasks[0]["priority"] == "alta"


def test_add_task_default_priority(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa comum")
    tasks = todo.load_tasks()
    assert tasks[0]["priority"] == "normal"


def test_export_tasks(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa exportada")
    export_path = tmp_path / "export.txt"
    todo.export_tasks(str(export_path))

    content = export_path.read_text(encoding="utf-8")
    assert "Tarefa exportada" in content


def test_list_done_only(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa concluída")
    todo.add_task("Tarefa pendente")
    todo.mark_done(1)
    capsys.readouterr()
    todo.list_tasks(done_only=True)

    out = capsys.readouterr().out
    assert "Tarefa concluída" in out
    assert "Tarefa pendente" not in out


def test_mark_undone(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Lavar louça")
    todo.mark_done(1)
    todo.mark_undone(1)
    tasks = todo.load_tasks()
    assert tasks[0]["done"] is False


def test_add_multiple_tasks(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa A; Tarefa B; Tarefa C")
    tasks = todo.load_tasks()
    assert [t["description"] for t in tasks] == ["Tarefa A", "Tarefa B", "Tarefa C"]


def test_add_task_invalid_priority(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa inválida", priority="urgentissimo")
    out = capsys.readouterr().out
    assert "Prioridade inválida" in out
    assert todo.load_tasks() == []


def test_count_tasks(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DB_PATH", tmp_path / "tasks.json")

    todo.add_task("Tarefa 1")
    todo.add_task("Tarefa 2")
    todo.mark_done(1)
    todo.count_tasks()

    out = capsys.readouterr().out
    assert "Total: 2" in out
    assert "Concluídas: 1" in out
    assert "Pendentes: 1" in out
