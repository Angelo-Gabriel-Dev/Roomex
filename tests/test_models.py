# tests/test_models.py
import pytest
from datetime import date
from roomex.models import Quarto, Hospede, Reserva, Pagamento, Adicional

# --- Testes de Quarto e Hospede (Mantidos) ---
def test_criar_quarto_valido():
    quarto = Quarto(101, "Simples", 2, 150.00)
    assert quarto.numero == 101

def test_validar_tarifa_negativa():
    with pytest.raises(ValueError, match="tarifa base deve ser maior"):
        Quarto(102, "Simples", 2, -50.00)

def test_heranca_hospede():
    """Testa se Hospede herda corretamente de Pessoa."""
    hospede = Hospede("João", "123", "email", "tel")
    assert hasattr(hospede, 'nome')
    assert hasattr(hospede, 'historico_reservas')

# --- Testes de Reserva (Atualizados com Pagamento/Adicional) ---
def test_fluxo_pagamentos_adicionais():
    """Testa adicionar pagamentos e lançar adicionais na reserva."""
    hospede = Hospede("Ana", "111", "email", "tel")
    quarto = Quarto(201, "Duplo", 2, 200.0)
    reserva = Reserva(hospede, quarto, 2, "site", date(2025, 1, 1), date(2025, 1, 5))

    # 1. Adicionar Pagamento
    reserva.adicionar_pagamento(100.00, "PIX", date(2025, 1, 1))
    assert len(reserva.pagamentos) == 1
    assert reserva.pagamentos[0].valor == 100.00
    assert reserva.pagamentos[0].forma == "PIX"

    # 2. Lançar Adicional
    reserva.lancar_adicional("Frigobar", 15.50)
    assert len(reserva.adicionais) == 1
    assert reserva.adicionais[0].descricao == "Frigobar"
    assert reserva.adicionais[0].valor == 15.50

def test_validar_datas_reserva():
    hospede = Hospede("Teste", "000", "e", "t")
    quarto = Quarto(101, "S", 2, 100)
    with pytest.raises(ValueError, match="anterior"):
        # Saída antes da entrada
        Reserva(hospede, quarto, 1, "site", date(2025, 1, 10), date(2025, 1, 5))