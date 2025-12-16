import pytest
from datetime import date, timedelta
from roomex.models import Quarto, Hospede, Reserva

# --- Fixtures (Dados prontos para usar nos testes) ---
@pytest.fixture
def hospede_teste():
    return Hospede("Tester", "000", "t@t.com", "00")

@pytest.fixture
def quarto_teste():
    return Quarto(900, "Teste", 1, 100.00) # Tarifa base R$ 100

# --- Testes de Regras de Negócio (Preço) ---

def test_calculo_fim_de_semana(hospede_teste, quarto_teste):
    """Testa se sábado/domingo fica mais caro (conforme settings.json padrão 1.2x)"""
    # 08/03/2025 é Sábado -> Deve custar 120.00
    reserva = Reserva(hospede_teste, quarto_teste, 1, "App", date(2025, 3, 8), date(2025, 3, 9))
    
    # Assumindo que settings.json existe e tem multiplicador 1.2
    # Se não existir, vai dar 100.00 e o teste avisa
    valor = reserva.calcular_valor_total()
    
    # Verificamos se aplicou algum aumento (maior que a tarifa base)
    assert valor > 100.00 

def test_multa_cancelamento(hospede_teste, quarto_teste):
    """Testa se cancelar gera multa"""
    reserva = Reserva(hospede_teste, quarto_teste, 1, "App", date(2025, 5, 1), date(2025, 5, 2))
    reserva.cancelar_reserva()
    
    assert reserva.status == "CANCELADA"
    # Verifica se um adicional (a multa) foi lançado
    assert len(reserva.adicionais) > 0
    assert reserva.adicionais[0].descricao == "Multa de Cancelamento"

# --- Testes de Fluxo (Status) ---

def test_ciclo_vida_reserva(hospede_teste, quarto_teste):
    """Testa o caminho feliz: Checkin -> Pagamento -> Checkout"""
    # 1. Criação
    reserva = Reserva(hospede_teste, quarto_teste, 1, "App", date(2025, 6, 1), date(2025, 6, 2))
    assert reserva.status == "PENDENTE"
    
    # 2. Check-in
    reserva.realizar_checkin()
    assert reserva.status == "ATIVA"
    
    # 3. Tentar Check-out sem pagar (Deve falhar)
    with pytest.raises(ValueError, match="Pagamento pendente"):
        reserva.realizar_checkout()
        
    # 4. Pagar
    total = reserva.calcular_valor_total()
    reserva.adicionar_pagamento(total, "Pix", date.today())
    
    # 5. Check-out com sucesso
    reserva.realizar_checkout()
    assert reserva.status == "FINALIZADA"