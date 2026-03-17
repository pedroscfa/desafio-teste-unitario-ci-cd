#!/usr/bin/env python3
"""CRUD simples de tarefas: título, descrição e data.""

from datetime import datetime
from typing import Dict, List, Optional


class Tarefa:
    def __init__(self, id_: int, titulo: str, descricao: str, data: str):
        self.id = id_
        self.titulo = titulo.strip()
        self.descricao = descricao.strip()
        self.data = data.strip()

    def __repr__(self):
        return (
            f"Tarefa(id={self.id}, titulo={self.titulo!r}, descricao={self.descricao!r}, data={self.data!r})"
        )

    def exibir(self):
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Descrição: {self.descricao}\n"
            f"Data: {self.data}\n"
            "------------------------------"
        )


def validar_data(data_texto: str) -> bool:
    try:
        datetime.strptime(data_texto.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def entrada_data(prompt_text: str) -> str:
    while True:
        valor = input(prompt_text).strip()
        if not valor:
            print("Data não pode ficar em branco. Use o formato YYYY-MM-DD.")
            continue
        if not validar_data(valor):
            print("Formato inválido. Use YYYY-MM-DD.")
            continue
        return valor


def criar_tarefa(tarefas: Dict[int, Tarefa], next_id: int) -> int:
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    data = entrada_data("Data (YYYY-MM-DD): ")
    tarefa = Tarefa(next_id, titulo, descricao, data)
    tarefas[next_id] = tarefa
    print(f"Tarefa criada com ID: {next_id}")
    return next_id + 1


def listar_tarefas(tarefas: Dict[int, Tarefa]) -> None:
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    print("\n=== Lista de Tarefas ===")
    for tarefa in tarefas.values():
        print(tarefa.exibir())


def obter_id_existente(tarefas: Dict[int, Tarefa]) -> Optional[int]:
    if not tarefas:
        print("Nenhuma tarefa para selecionar.")
        return None
    try:
        id_texto = input("Informe o ID da tarefa: ").strip()
        id_tarefa = int(id_texto)
        if id_tarefa not in tarefas:
            print("ID não encontrado.")
            return None
        return id_tarefa
    except ValueError:
        print("ID inválido.")
        return None


def atualizar_tarefa(tarefas: Dict[int, Tarefa]) -> None:
    id_tarefa = obter_id_existente(tarefas)
    if id_tarefa is None:
        return
    tarefa = tarefas[id_tarefa]
    print("Digite novo valor ou enter para manter o existente.")
    novo_titulo = input(f"Título ({tarefa.titulo}): ").strip() or tarefa.titulo
    nova_descricao = input(f"Descrição ({tarefa.descricao}): ").strip() or tarefa.descricao
    nova_data = input(f"Data ({tarefa.data}, formato YYYY-MM-DD): ").strip() or tarefa.data
    if nova_data and not validar_data(nova_data):
        print("Data inválida. Atualização cancelada.")
        return
    tarefa.titulo = novo_titulo
    tarefa.descricao = nova_descricao
    tarefa.data = nova_data
    print("Tarefa atualizada com sucesso.")


def deletar_tarefa(tarefas: Dict[int, Tarefa]) -> None:
    id_tarefa = obter_id_existente(tarefas)
    if id_tarefa is None:
        return
    confirm = input(f"Tem certeza que deseja excluir a tarefa {id_tarefa}? (s/n): ").lower().strip()
    if confirm == "s":
        del tarefas[id_tarefa]
        print("Tarefa excluída.")
    else:
        print("Exclusão cancelada.")


def menu() -> None:
    tarefas: Dict[int, Tarefa] = {}
    proximo_id = 1
    while True:
        print("\n=== CRUD de Tarefas ===")
        print("1. Criar tarefa")
        print("2. Listar tarefas")
        print("3. Atualizar tarefa")
        print("4. Deletar tarefa")
        print("5. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            proximo_id = criar_tarefa(tarefas, proximo_id)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            atualizar_tarefa(tarefas)
        elif opcao == "4":
            deletar_tarefa(tarefas)
        elif opcao == "5":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
