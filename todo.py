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


def add_task(description, priority="normal"):
    tasks = load_tasks()
    tasks.append({"description": description, "done": False, "priority": priority})
    save_tasks(tasks)
    print(f"Tarefa adicionada [{priority}]: {description}")


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
        priority = task.get("priority", "normal")
        print(f"[{status}] {i}. ({priority}) {task['description']}")
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


def search_tasks(query):
    tasks = load_tasks()
    matches = [
        (i, task) for i, task in enumerate(tasks, start=1)
        if query.lower() in task["description"].lower()
    ]
    if not matches:
        print(f"Nenhuma tarefa encontrada para: {query}")
        return
    for i, task in matches:
        status = "x" if task["done"] else " "
        priority = task.get("priority", "normal")
        print(f"[{status}] {i}. ({priority}) {task['description']}")


def edit_task(index, new_description):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Tarefa {index} não encontrada.")
        return
    tasks[index - 1]["description"] = new_description
    save_tasks(tasks)
    print(f"Tarefa {index} atualizada: {new_description}")


def count_tasks():
    tasks = load_tasks()
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    print(f"Total: {total} | Concluídas: {done} | Pendentes: {pending}")


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
            print("Uso: python todo.py add <descrição> [--priority alta|normal|baixa]")
            return
        args = sys.argv[2:]
        priority = "normal"
        if "--priority" in args:
            idx = args.index("--priority")
            priority = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        add_task(" ".join(args), priority=priority)
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
    elif command == "count":
        count_tasks()
    elif command == "edit":
        if len(sys.argv) < 4:
            print("Uso: python todo.py edit <número> <nova descrição>")
            return
        edit_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "search":
        if len(sys.argv) < 3:
            print("Uso: python todo.py search <termo>")
            return
        search_tasks(" ".join(sys.argv[2:]))
    else:
        print(f"Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
