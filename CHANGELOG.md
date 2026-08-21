# Changelog

## 0.1.0

- CLI inicial com comandos `add` e `list`.
- Comandos `done` e `remove`.
- Comando `clear` para limpar todas as tarefas.
- Filtro `--pending` no comando `list`.
- Comando `edit` para editar a descrição de uma tarefa.
- Comando `search` para buscar tarefas por texto.
- Campo de prioridade nas tarefas (`--priority` no `add`).
- Workflow de CI para rodar os testes automaticamente.

## 0.2.0

- Comando `count` com total de tarefas, concluídas e pendentes.
- Validação de prioridade em `add`.
- Comando `stats` com percentual de conclusão.
- Filtro `--sort-priority` no comando `list`.
- Comando `rename` como alias de `edit`.
- Suporte a múltiplas tarefas em `add` separadas por `;`.
- Comando `undone` para desmarcar tarefas concluídas.
- Filtro `--done` no comando `list`.
- Mensagem de erro amigável para índices inválidos.
