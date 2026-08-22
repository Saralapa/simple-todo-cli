import json
import sys
from datetime import date
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


VALID_PRIORITIES = ("alta", "normal", "baixa")


def add_task(description, priority="normal", due=None):
    if priority not in VALID_PRIORITIES:
        print(f"Prioridade inválida: {priority}. Use uma de: {', '.join(VALID_PRIORITIES)}")
        return
    descriptions = [d.strip() for d in description.split(";") if d.strip()]
    if not descriptions:
        return
    tasks = load_tasks()
    for desc in descriptions:
        task = {"description": desc, "done": False, "priority": priority}
        if due:
            task["due"] = due
        tasks.append(task)
        suffix = f" (prazo: {due})" if due else ""
        print(f"Tarefa adicionada [{priority}]: {desc}{suffix}")
    save_tasks(tasks)


PRIORITY_ORDER = {"alta": 0, "normal": 1, "baixa": 2}


def list_tasks(pending_only=False, sort_priority=False, done_only=False):
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa cadastrada.")
        return
    indexed = list(enumerate(tasks, start=1))
    if sort_priority:
        indexed.sort(key=lambda pair: PRIORITY_ORDER.get(pair[1].get("priority", "normal"), 1))
    shown = False
    for i, task in indexed:
        if pending_only and task["done"]:
            continue
        if done_only and not task["done"]:
            continue
        status = "x" if task["done"] else " "
        priority = task.get("priority", "normal")
        due_suffix = f" (prazo: {task['due']})" if task.get("due") else ""
        print(f"[{status}] {i}. ({priority}) {task['description']}{due_suffix}")
        shown = True
    if pending_only and not shown:
        print("Nenhuma tarefa pendente.")
    elif done_only and not shown:
        print("Nenhuma tarefa concluída.")


def _validate_index(tasks, index):
    if index < 1 or index > len(tasks):
        print(f"Tarefa {index} não encontrada.")
        return False
    return True


def mark_done(index):
    tasks = load_tasks()
    if not _validate_index(tasks, index):
        return
    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    print(f"Tarefa {index} marcada como concluída.")


def mark_undone(index):
    tasks = load_tasks()
    if not _validate_index(tasks, index):
        return
    tasks[index - 1]["done"] = False
    save_tasks(tasks)
    print(f"Tarefa {index} marcada como pendente.")


def remove_task(index):
    tasks = load_tasks()
    if not _validate_index(tasks, index):
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Tarefa removida: {removed['description']}")


def duplicate_task(index):
    tasks = load_tasks()
    if not _validate_index(tasks, index):
        return
    clone = dict(tasks[index - 1])
    clone["done"] = False
    tasks.append(clone)
    save_tasks(tasks)
    print(f"Tarefa duplicada: {clone['description']}")


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
    if not _validate_index(tasks, index):
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


def show_stats():
    tasks = load_tasks()
    total = len(tasks)
    if total == 0:
        print("Nenhuma tarefa cadastrada.")
        return
    done = sum(1 for t in tasks if t["done"])
    percent = (done / total) * 100
    print(f"Progresso: {done}/{total} ({percent:.1f}%)")


def import_tasks(path):
    import_path = Path(path)
    if not import_path.exists():
        print(f"Arquivo não encontrado: {import_path}")
        return
    with open(import_path, "r", encoding="utf-8") as f:
        imported = json.load(f)
    tasks = load_tasks()
    tasks.extend(imported)
    save_tasks(tasks)
    print(f"{len(imported)} tarefa(s) importada(s) de: {import_path}")


def export_tasks(path):
    tasks = load_tasks()
    export_path = Path(path)
    with open(export_path, "w", encoding="utf-8") as f:
        for i, task in enumerate(tasks, start=1):
            status = "x" if task["done"] else " "
            priority = task.get("priority", "normal")
            f.write(f"[{status}] {i}. ({priority}) {task['description']}\n")
    print(f"Tarefas exportadas para: {export_path}")


def list_overdue(today=None):
    today = today or date.today().isoformat()
    tasks = load_tasks()
    matches = [
        (i, task) for i, task in enumerate(tasks, start=1)
        if not task["done"] and task.get("due") and task["due"] < today
    ]
    if not matches:
        print("Nenhuma tarefa vencida.")
        return
    for i, task in matches:
        priority = task.get("priority", "normal")
        print(f"[ ] {i}. ({priority}) {task['description']} (prazo: {task['due']})")


def clear_tasks(done_only=False):
    if not done_only:
        save_tasks([])
        print("Todas as tarefas foram removidas.")
        return
    tasks = load_tasks()
    remaining = [t for t in tasks if not t["done"]]
    removed_count = len(tasks) - len(remaining)
    save_tasks(remaining)
    print(f"{removed_count} tarefa(s) concluída(s) removida(s).")


def _parse_index(raw):
    try:
        return int(raw)
    except ValueError:
        print(f"Número de tarefa inválido: {raw}")
        return None


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
        due = None
        if "--due" in args:
            idx = args.index("--due")
            due = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        add_task(" ".join(args), priority=priority, due=due)
    elif command == "list":
        pending_only = "--pending" in sys.argv[2:]
        sort_priority = "--sort-priority" in sys.argv[2:]
        done_only = "--done" in sys.argv[2:]
        list_tasks(pending_only=pending_only, sort_priority=sort_priority, done_only=done_only)
    elif command == "done":
        if len(sys.argv) < 3:
            print("Uso: python todo.py done <número>")
            return
        index = _parse_index(sys.argv[2])
        if index is not None:
            mark_done(index)
    elif command == "undone":
        if len(sys.argv) < 3:
            print("Uso: python todo.py undone <número>")
            return
        index = _parse_index(sys.argv[2])
        if index is not None:
            mark_undone(index)
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Uso: python todo.py remove <número>")
            return
        index = _parse_index(sys.argv[2])
        if index is not None:
            remove_task(index)
    elif command == "clear":
        done_only = "--done" in sys.argv[2:]
        clear_tasks(done_only=done_only)
    elif command == "overdue":
        list_overdue()
    elif command == "duplicate":
        if len(sys.argv) < 3:
            print("Uso: python todo.py duplicate <número>")
            return
        index = _parse_index(sys.argv[2])
        if index is not None:
            duplicate_task(index)
    elif command == "count":
        count_tasks()
    elif command == "stats":
        show_stats()
    elif command == "export":
        if len(sys.argv) < 3:
            print("Uso: python todo.py export <arquivo.txt>")
            return
        export_tasks(sys.argv[2])
    elif command == "import":
        if len(sys.argv) < 3:
            print("Uso: python todo.py import <arquivo.json>")
            return
        import_tasks(sys.argv[2])
    elif command in ("edit", "rename"):
        if len(sys.argv) < 4:
            print(f"Uso: python todo.py {command} <número> <nova descrição>")
            return
        index = _parse_index(sys.argv[2])
        if index is not None:
            edit_task(index, " ".join(sys.argv[3:]))
    elif command == "search":
        if len(sys.argv) < 3:
            print("Uso: python todo.py search <termo>")
            return
        search_tasks(" ".join(sys.argv[2:]))
    else:
        print(f"Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
