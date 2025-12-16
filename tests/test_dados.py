# tests/test_dados.py
import pytest
import os
from datetime import date
from roomex.models import Quarto, Hospede
from roomex.dados import salvar_dados, carregar_dados

def test_salvar_e_carregar_quartos(tmp_path):
    """
    Testa o ciclo completo de persistência usando um arquivo temporário.
    O 'tmp_path' é uma fixture do pytest que cria uma pasta temporária que se apaga sozinha.
    """
    # 1. Criar dados em memória
    quartos_originais = [
        Quarto(101, "Simples", 1, 100.0),
        Quarto(102, "Luxo", 2, 500.0)
    ]
    
    # 2. Definir arquivo temporário
    arquivo_teste = tmp_path / "quartos_teste.json"
    
    # 3. Salvar
    salvar_dados(quartos_originais, str(arquivo_teste))
    
    # 4. Verificar se arquivo foi criado
    assert os.path.exists(arquivo_teste)
    
    # 5. Carregar de volta
    quartos_carregados = carregar_dados(str(arquivo_teste), Quarto)
    
    # 6. Conferir se os dados batem
    assert len(quartos_carregados) == 2
    assert quartos_carregados[0].numero == 101
    assert quartos_carregados[1].tipo == "Luxo"
    assert quartos_carregados[1].tarifa_base == 500.0

def test_carregar_arquivo_inexistente():
    resultado = carregar_dados("arquivo_fantasma.json", Quarto)
    assert resultado == []