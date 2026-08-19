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


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa cadastrada.")
        return
    for i, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['description']}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python todo.py <add|list> [argumentos]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Uso: python todo.py add <descrição>")
            return
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    else:
        print(f"Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
