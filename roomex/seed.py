from roomex.models import Quarto
from roomex.dados import salvar_dados
import os

def criar_dados_iniciais():
    """
    Gera dados iniciais (Seed) para o sistema e salva em JSON.
    """
    print("🌱 Iniciando o Seed (populando o banco de dados)...")

    # 1. Criando 8 Quartos com dados variados
    quartos = [
        # Quartos Simples (Capacidade 1-2)
        Quarto(numero=101, tipo="SIMPLES", capacidade=1, tarifa_base=100.00),
        Quarto(numero=102, tipo="SIMPLES", capacidade=1, tarifa_base=100.00),
        Quarto(numero=103, tipo="SIMPLES", capacidade=2, tarifa_base=120.00),
        
        # Quartos Duplos (Capacidade 2-3)
        Quarto(numero=201, tipo="DUPLO", capacidade=2, tarifa_base=180.00),
        Quarto(numero=202, tipo="DUPLO", capacidade=2, tarifa_base=180.00),
        Quarto(numero=203, tipo="DUPLO", capacidade=3, tarifa_base=200.00),

        # Quartos de Luxo (Capacidade 4)
        Quarto(numero=301, tipo="LUXO", capacidade=4, tarifa_base=450.00),
        Quarto(numero=302, tipo="LUXO", capacidade=4, tarifa_base=450.00),
    ]

    # 2. Definindo o caminho do arquivo
    # Salva na raiz do projeto ou em uma pasta 'data' se preferir
    arquivo_quartos = "quartos.json"

    # 3. Salvando usando a função do dados.py
    salvar_dados(quartos, arquivo_quartos)
    
    print(f"✅ Sucesso! {len(quartos)} quartos foram salvos em '{arquivo_quartos}'.")

if __name__ == "__main__":
    criar_dados_iniciais()