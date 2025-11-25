import pytest
from datetime import date
from roomex.models import Quarto, Hospede, Reserva

# --- Testes da Classe Quarto ---

def test_criar_quarto_valido():
    """Testa se um quarto é criado corretamente com dados válidos."""
    quarto = Quarto(101, "Simples", 2, 150.00)
    assert quarto.numero == 101
    assert quarto.capacidade == 2
    assert quarto.tarifa_base == 150.00

def test_validar_tarifa_negativa():
    """Testa se o sistema impede a criação de quarto com tarifa negativa."""
    with pytest.raises(ValueError, match="tarifa base deve ser maior que zero"):
        Quarto(102, "Simples", 2, -50.00)

def test_validar_capacidade_invalida():
    """Testa se o sistema impede capacidade menor que 1."""
    with pytest.raises(ValueError, match="capacidade deve ser de pelo menos 1"):
        Quarto(103, "Duplo", 0, 200.00)

def test_representacao_string_quarto():
    """Testa se o __str__ do quarto retorna o texto formatado."""
    quarto = Quarto(101, "Luxo", 2, 500.0)
    # Verifica se o texto retornado contém as informações principais
    assert "Quarto 101" in str(quarto)
    assert "Luxo" in str(quarto)
    assert "500.00" in str(quarto)

def test_ordenacao_quartos():
    """Testa se o __lt__ ordena os quartos pelo número."""
    q1 = Quarto(100, "Simples", 1, 100)
    q2 = Quarto(200, "Duplo", 2, 200)
    assert q1 < q2  # 100 é menor que 200

# --- Testes da Classe Reserva ---

def test_criar_reserva_valida():
    """Testa a criação de uma reserva com datas e capacidade corretas."""
    hospede = Hospede("João", "123", "email", "tel")
    quarto = Quarto(101, "Simples", 2, 100.0)
    
    entrada = date(2025, 1, 1)
    saida = date(2025, 1, 5)
    
    reserva = Reserva(hospede, quarto, 2, "site", entrada, saida)
    
    assert reserva.status == "PENDENTE"
    assert len(reserva) == 4  # 4 diárias

def test_erro_data_saida_antes_entrada():
    """Testa se lança erro ao tentar reservar com saída antes da entrada."""
    hospede = Hospede("Maria", "456", "email", "tel")
    quarto = Quarto(101, "Simples", 2, 100.0)
    
    entrada = date(2025, 1, 10)
    saida = date(2025, 1, 5)

    with pytest.raises(ValueError, match="data de entrada deve ser anterior"):
        Reserva(hospede, quarto, 1, "site", entrada, saida)

def test_erro_capacidade_excedida():
    """Testa se lança erro ao colocar mais hóspedes que a capacidade do quarto."""
    hospede = Hospede("Pedro", "789", "email", "tel")
    quarto = Quarto(101, "Simples", 2, 100.0) # Capacidade é 2
    
    with pytest.raises(ValueError, match="suporta apenas 2 pessoas"):
        # Tentando colocar 3 pessoas em um quarto de 2
        Reserva(hospede, quarto, 3, "site", date(2025, 1, 1), date(2025, 1, 2))

def test_reserva_len():
    """Testa se o método __len__ calcula os dias corretamente."""
    hospede = Hospede("Teste", "000", "e", "t")
    quarto = Quarto(101, "S", 2, 100)
    
    # 10 dias de diferença
    r = Reserva(hospede, quarto, 1, "site", date(2025, 1, 1), date(2025, 1, 11))
    assert len(r) == 10