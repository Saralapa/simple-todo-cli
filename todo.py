import json
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "done": False})
    save_tasks(tasks)
    print(f"Tarefa adicionada: {description}")


def list_tasks(pending_only=False):
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa cadastrada.")
        return
    shown = False
    for i, task in enumerate(tasks, start=1):
        if pending_only and task["done"]:
            continue
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['description']}")
        shown = True
    if pending_only and not shown:
        print("Nenhuma tarefa pendente.")


def mark_done(index):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Tarefa {index} não encontrada.")
        return
    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    print(f"Tarefa {index} marcada como concluída.")


def remove_task(index):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Tarefa {index} não encontrada.")
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Tarefa removida: {removed['description']}")


def clear_tasks():
    save_tasks([])
    print("Todas as tarefas foram removidas.")


def main():
    if len(sys.argv) < 2:
        print("Uso: python todo.py <add|list|done|remove|clear> [argumentos]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Uso: python todo.py add <descrição>")
            return
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        pending_only = "--pending" in sys.argv[2:]
        list_tasks(pending_only=pending_only)
    elif command == "done":
        if len(sys.argv) < 3:
            print("Uso: python todo.py done <número>")
            return
        mark_done(int(sys.argv[2]))
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Uso: python todo.py remove <número>")
            return
        remove_task(int(sys.argv[2]))
    elif command == "clear":
        clear_tasks()
    else:
        print(f"Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
