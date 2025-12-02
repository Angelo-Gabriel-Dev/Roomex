# tests/test_reports.py
import pytest
from datetime import date
from roomex.models import Quarto, Hospede, Reserva
from roomex.reports import calcular_taxa_ocupacao

def test_calculo_taxa_ocupacao():
    """
    Cenário: Hotel com 2 quartos. Relatório de 5 dias. Total de diárias possíveis: 10.
    Reserva 1: Ocupa 5 dias do Quarto 1.
    Reserva 2: Ocupa 0 dias (está fora do período).
    Resultado esperado: 50% de ocupação (5 dias ocupados de 10 possíveis).
    """
    # Setup
    hospede = Hospede("Test", "123", "e", "t")
    q1 = Quarto(101, "S", 2, 100)
    q2 = Quarto(102, "S", 2, 100)
    
    # Reserva dentro do período (1 a 6 de Jan = 5 diárias)
    r1 = Reserva(hospede, q1, 1, "site", date(2025, 1, 1), date(2025, 1, 6))
    
    # Reserva fora do período (fevereiro)
    r2 = Reserva(hospede, q2, 1, "site", date(2025, 2, 1), date(2025, 2, 5))
    
    lista_reservas = [r1, r2]
    
    # Execução
    taxa = calcular_taxa_ocupacao(
        reservas=lista_reservas, 
        data_inicio=date(2025, 1, 1), 
        data_fim=date(2025, 1, 6), # 5 dias de intervalo
        total_quartos=2
    )
    
    # Asserts
    assert taxa == 50.0  # (5 dias ocupados / 10 dias totais) * 100

def test_ocupacao_vazia():
    taxa = calcular_taxa_ocupacao([], date(2025, 1, 1), date(2025, 1, 5), 10)
    assert taxa == 0.0