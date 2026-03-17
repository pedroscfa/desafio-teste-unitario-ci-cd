# Desafio Teste Unitário — CI/CD

![CI](https://github.com/SEU_USUARIO/desafio-teste-unitario-id/actions/workflows/ci.yml/badge.svg)

CRUD simples de tarefas em Python com testes unitários e pipeline de CI/CD via GitHub Actions.

---

## 📁 Estrutura do projeto

```
├── tarefas_crud.py        # Código principal
├── test_tarefas.py        # Testes unitários
├── README.md
└── .github/
    └── workflows/
        └── ci.yml         # Pipeline de CI/CD
```

---

## ▶️ Como rodar localmente

**Instalar dependências:**
```bash
pip install pytest
```

**Executar os testes:**
```bash
pytest test_tarefas.py -v
```

**Executar com cobertura:**
```bash
pip install pytest-cov
pytest test_tarefas.py --cov=tarefas_crud --cov-report=term-missing
```

---

## 🧪 Cobertura dos testes

| Módulo | Cenários testados |
|---|---|
| `Tarefa` construtor | strip, vazio, só espaços, atributos corretos |
| `Tarefa.exibir()` | todos os campos presentes no formato esperado |
| `validar_data` | válida, vazia, formatos errados, ano bissexto |
| `criar_tarefa` | adição ao dict, incremento de ID, dados corretos |
| `listar_tarefas` | lista vazia, uma tarefa, múltiplas tarefas |
| `obter_id_existente` | válido, inexistente, não numérico, negativo, zero |
| `atualizar_tarefa` | parcial, campo vazio mantém original, data inválida cancela |
| `deletar_tarefa` | confirma "s", cancela "n", ID não reutilizado |

---

## ⚙️ Pipeline CI/CD

A pipeline executa automaticamente a cada `push` em qualquer branch.

**Passos executados:**
1. Checkout do repositório
2. Configuração do Python 3.11
3. Instalação do `pytest` e `pytest-cov`
4. Execução dos testes com relatório detalhado
5. Relatório de cobertura de código
