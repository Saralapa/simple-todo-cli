# simple-todo-cli

Um pequeno CLI de lista de tarefas escrito em Python. Armazena as tarefas em um arquivo JSON local.

## Uso

```
python todo.py add "Comprar pão"
python todo.py add "Pagar contas" --priority alta
python todo.py list
python todo.py list --pending
python todo.py done 1
python todo.py edit 1 "Comprar pão integral"
python todo.py search pão
python todo.py remove 1
python todo.py clear
```

## Testes

```
pip install pytest
pytest
```
