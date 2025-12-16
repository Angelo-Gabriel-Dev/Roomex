import pytest
from datetime import date
from roomex.models import Quarto, Hospede, Reserva
from roomex.reports import calcular_metricas_financeiras, relatorio_cancelamentos

# --- Fixtures (Dados Fakes) ---
@pytest.fixture
def dados_cenario():
    q1 = Quarto(101, "Simples", 1, 100.00)
    q2 = Quarto(102, "Simples", 1, 100.00)
    hospede = Hospede("Tester", "000", "t@t.com", "00")
    return [q1, q2], hospede

def test_calculo_adr_revpar(dados_cenario):
    quartos, hospede = dados_cenario
    
    # MUDANÇA: Usando ABRIL (Mês 4) para evitar a Alta Temporada de Janeiro do settings.json
    # Período do Relatório: 01/04 a 03/04 (2 noites)
    
    # Reserva 1: Confirmada (Gera Receita)
    r1 = Reserva(hospede, quartos[0], 1, "Site", date(2025, 4, 1), date(2025, 4, 3))
    r1.status = "CONFIRMADA"
    
    # Reserva 2: Cancelada (Não conta na receita)
    r2 = Reserva(hospede, quartos[1], 1, "Site", date(2025, 4, 1), date(2025, 4, 3))
    r2.status = "CANCELADA"
    
    lista_reservas = [r1, r2]
    
    # Executa o cálculo
    metricas = calcular_metricas_financeiras(
        lista_reservas, 
        date(2025, 4, 1), 
        date(2025, 4, 3), 
        total_quartos=2
    )
    
    # VALIDAÇÕES:
    # Receita: 2 diárias de R$ 100 (sem multiplicador) = R$ 200.00
    assert metricas["receita_total"] == 200.00
    
    # Ocupação: 2 dias ocupados / 4 dias disponíveis (2 quartos * 2 dias) = 50%
    assert metricas["ocupacao"] == 50.0
    
    # ADR: Receita (200) / Dias Vendidos (2) = 100.00
    assert metricas["adr"] == 100.00
    
    # RevPAR: Receita (200) / Inventário Total (4) = 50.00
    assert metricas["revpar"] == 50.00

def test_contagem_cancelamentos(dados_cenario):
    quartos, hospede = dados_cenario
    
    # Datas genéricas
    r1 = Reserva(hospede, quartos[0], 1, "Site", date(2025, 4, 1), date(2025, 4, 2))
    r1.status = "CANCELADA"
    
    r2 = Reserva(hospede, quartos[0], 1, "Site", date(2025, 4, 1), date(2025, 4, 2))
    r2.status = "NO_SHOW"
    
    r3 = Reserva(hospede, quartos[0], 1, "Site", date(2025, 4, 1), date(2025, 4, 2))
    r3.status = "ATIVA"
    
    stats = relatorio_cancelamentos([r1, r2, r3], date(2025, 4, 1), date(2025, 4, 5))
    
    assert stats["CANCELADA"] == 1
    assert stats["NO_SHOW"] == 1
    assert stats["TOTAL"] == 2