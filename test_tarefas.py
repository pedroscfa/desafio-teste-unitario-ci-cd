#!/usr/bin/env python3
"""Testes unitários para o CRUD de tarefas."""

import pytest
from unittest.mock import patch
from tarefas import (
    Tarefa,
    validar_data,
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    deletar_tarefa,
    obter_id_existente,
)


# ===========================================================================
# Tarefa — construtor e métodos
# ===========================================================================

class TestTarefaConstrutor:
    def test_strip_titulo(self):
        t = Tarefa(1, "  Compras  ", "desc", "2024-01-01")
        assert t.titulo == "Compras"

    def test_strip_descricao(self):
        t = Tarefa(1, "Título", "  Fazer lista  ", "2024-01-01")
        assert t.descricao == "Fazer lista"

    def test_strip_data(self):
        t = Tarefa(1, "Título", "desc", "  2024-01-01  ")
        assert t.data == "2024-01-01"

    def test_atributos_corretos(self):
        t = Tarefa(42, "Reunião", "Daily", "2025-03-17")
        assert t.id == 42
        assert t.titulo == "Reunião"
        assert t.descricao == "Daily"
        assert t.data == "2025-03-17"

    def test_titulo_vazio(self):
        t = Tarefa(1, "", "desc", "2024-01-01")
        assert t.titulo == ""

    def test_titulo_apenas_espacos(self):
        t = Tarefa(1, "   ", "desc", "2024-01-01")
        assert t.titulo == ""


class TestTarefaExibir:
    def test_exibir_contem_id(self):
        t = Tarefa(5, "Título", "Desc", "2024-06-01")
        assert "5" in t.exibir()

    def test_exibir_contem_titulo(self):
        t = Tarefa(1, "Reunião", "Desc", "2024-06-01")
        assert "Reunião" in t.exibir()

    def test_exibir_contem_descricao(self):
        t = Tarefa(1, "Título", "Fazer ata", "2024-06-01")
        assert "Fazer ata" in t.exibir()

    def test_exibir_contem_data(self):
        t = Tarefa(1, "Título", "Desc", "2024-06-01")
        assert "2024-06-01" in t.exibir()

    def test_exibir_formato_completo(self):
        t = Tarefa(1, "Título", "Desc", "2024-06-01")
        saida = t.exibir()
        assert "ID:" in saida
        assert "Título:" in saida
        assert "Descrição:" in saida
        assert "Data:" in saida


# ===========================================================================
# validar_data
# ===========================================================================

class TestValidarData:
    def test_data_valida(self):
        assert validar_data("2024-01-15") is True

    def test_data_vazia(self):
        assert validar_data("") is False

    def test_formato_brasileiro(self):
        assert validar_data("15/01/2024") is False

    def test_formato_americano(self):
        assert validar_data("01-15-2024") is False

    def test_data_inexistente(self):
        assert validar_data("2024-02-30") is False

    def test_ano_bissexto_valido(self):
        assert validar_data("2024-02-29") is True

    def test_ano_nao_bissexto_invalido(self):
        assert validar_data("2023-02-29") is False

    def test_data_com_espacos(self):
        assert validar_data("  2024-01-01  ") is True

    def test_texto_aleatorio(self):
        assert validar_data("não-é-data") is False

    def test_apenas_ano(self):
        assert validar_data("2024") is False


# ===========================================================================
# criar_tarefa
# ===========================================================================

class TestCriarTarefa:
    def test_tarefa_adicionada_ao_dicionario(self):
        tarefas = {}
        with patch("builtins.input", side_effect=["Título", "Descrição", "2024-01-01"]):
            criar_tarefa(tarefas, 1)
        assert 1 in tarefas

    def test_next_id_incrementado(self):
        tarefas = {}
        with patch("builtins.input", side_effect=["Título", "Descrição", "2024-01-01"]):
            novo_id = criar_tarefa(tarefas, 1)
        assert novo_id == 2

    def test_ids_sequenciais_multiplas_tarefas(self):
        tarefas = {}
        with patch("builtins.input", side_effect=["T1", "D1", "2024-01-01"]):
            next_id = criar_tarefa(tarefas, 1)
        with patch("builtins.input", side_effect=["T2", "D2", "2024-02-01"]):
            next_id = criar_tarefa(tarefas, next_id)
        assert 1 in tarefas
        assert 2 in tarefas

    def test_dados_salvos_corretamente(self):
        tarefas = {}
        with patch("builtins.input", side_effect=["Reunião", "Daily", "2024-05-10"]):
            criar_tarefa(tarefas, 1)
        t = tarefas[1]
        assert t.titulo == "Reunião"
        assert t.descricao == "Daily"
        assert t.data == "2024-05-10"

    def test_titulo_vazio_aceito(self):
        """O código atual aceita título vazio — teste documenta esse comportamento."""
        tarefas = {}
        with patch("builtins.input", side_effect=["", "Descrição", "2024-01-01"]):
            criar_tarefa(tarefas, 1)
        assert tarefas[1].titulo == ""


# ===========================================================================
# listar_tarefas
# ===========================================================================

class TestListarTarefas:
    def test_lista_vazia(self, capsys):
        listar_tarefas({})
        saida = capsys.readouterr().out
        assert "Nenhuma tarefa" in saida

    def test_lista_com_uma_tarefa(self, capsys):
        tarefas = {1: Tarefa(1, "Título", "Desc", "2024-01-01")}
        listar_tarefas(tarefas)
        saida = capsys.readouterr().out
        assert "Título" in saida

    def test_lista_com_multiplas_tarefas(self, capsys):
        tarefas = {
            1: Tarefa(1, "Tarefa A", "Desc A", "2024-01-01"),
            2: Tarefa(2, "Tarefa B", "Desc B", "2024-02-01"),
        }
        listar_tarefas(tarefas)
        saida = capsys.readouterr().out
        assert "Tarefa A" in saida
        assert "Tarefa B" in saida


# ===========================================================================
# obter_id_existente
# ===========================================================================

class TestObterIdExistente:
    def test_id_valido_retorna_id(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="1"):
            resultado = obter_id_existente(tarefas)
        assert resultado == 1

    def test_id_inexistente_retorna_none(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="99"):
            resultado = obter_id_existente(tarefas)
        assert resultado is None

    def test_id_nao_numerico_retorna_none(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="abc"):
            resultado = obter_id_existente(tarefas)
        assert resultado is None

    def test_dicionario_vazio_retorna_none(self):
        with patch("builtins.input", return_value="1"):
            resultado = obter_id_existente({})
        assert resultado is None

    def test_id_negativo_retorna_none(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="-1"):
            resultado = obter_id_existente(tarefas)
        assert resultado is None

    def test_id_zero_retorna_none(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="0"):
            resultado = obter_id_existente(tarefas)
        assert resultado is None


# ===========================================================================
# atualizar_tarefa
# ===========================================================================

class TestAtualizarTarefa:
    def _tarefa_base(self):
        return {1: Tarefa(1, "Original", "Desc original", "2024-01-01")}

    def test_atualiza_titulo(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", side_effect=["1", "Novo Título", "", ""]):
            atualizar_tarefa(tarefas)
        assert tarefas[1].titulo == "Novo Título"

    def test_mantem_titulo_se_vazio(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", side_effect=["1", "", "", ""]):
            atualizar_tarefa(tarefas)
        assert tarefas[1].titulo == "Original"

    def test_atualiza_descricao(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", side_effect=["1", "", "Nova desc", ""]):
            atualizar_tarefa(tarefas)
        assert tarefas[1].descricao == "Nova desc"

    def test_atualiza_data_valida(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", side_effect=["1", "", "", "2025-12-31"]):
            atualizar_tarefa(tarefas)
        assert tarefas[1].data == "2025-12-31"

    def test_data_invalida_cancela_atualizacao(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", side_effect=["1", "Novo", "Nova desc", "data-errada"]):
            atualizar_tarefa(tarefas)
        # Nenhum campo deve ter sido alterado
        assert tarefas[1].titulo == "Original"
        assert tarefas[1].descricao == "Desc original"
        assert tarefas[1].data == "2024-01-01"

    def test_id_inexistente_nao_altera_nada(self):
        tarefas = self._tarefa_base()
        with patch("builtins.input", return_value="99"):
            atualizar_tarefa(tarefas)
        assert tarefas[1].titulo == "Original"


# ===========================================================================
# deletar_tarefa
# ===========================================================================

class TestDeletarTarefa:
    def test_deleta_com_confirmacao_s(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", side_effect=["1", "s"]):
            deletar_tarefa(tarefas)
        assert 1 not in tarefas

    def test_nao_deleta_com_confirmacao_n(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", side_effect=["1", "n"]):
            deletar_tarefa(tarefas)
        assert 1 in tarefas

    def test_id_nao_reutilizado_apos_delecao(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", side_effect=["1", "s"]):
            deletar_tarefa(tarefas)
        with patch("builtins.input", side_effect=["T2", "D2", "2024-02-01"]):
            novo_id = criar_tarefa(tarefas, 2)
        assert 2 in tarefas
        assert 1 not in tarefas
        assert novo_id == 3

    def test_id_inexistente_nao_altera_dicionario(self):
        tarefas = {1: Tarefa(1, "T", "D", "2024-01-01")}
        with patch("builtins.input", return_value="99"):
            deletar_tarefa(tarefas)
        assert len(tarefas) == 1
