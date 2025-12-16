import sys
import os
from datetime import date

# --- TRUQUE DE CAMINHO ---
# Adiciona a pasta raiz do projeto (..) ao caminho do Python
# Isso permite importar 'roomex' mesmo estando dentro de 'tests'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from roomex.models import Quarto, Hospede, Reserva

def testar_precos():
    print("--- 🧪 INICIANDO TESTE DE CÁLCULO DE PREÇOS (Manual) ---")
    
    # 1. Preparação
    hospede = Hospede("Testador", "000", "teste@email.com", "000")
    quarto = Quarto(999, "Teste", 1, 100.00) 

    # --- CASO 1: Dia Normal (Segunda-feira) ---
    r_normal = Reserva(hospede, quarto, 1, "site", date(2025, 3, 10), date(2025, 3, 11))
    valor_normal = r_normal.calcular_valor_total()
    print(f"\n1. Dia Normal (Esperado: 100.00)")
    print(f"   Resultado: R$ {valor_normal:.2f}")

    # --- CASO 2: Fim de Semana (Sábado) ---
    r_fds = Reserva(hospede, quarto, 1, "site", date(2025, 3, 8), date(2025, 3, 9))
    valor_fds = r_fds.calcular_valor_total()
    print(f"\n2. Fim de Semana (Esperado: 120.00 se config padrão)")
    print(f"   Resultado: R$ {valor_fds:.2f}")

    # --- CASO 3: Alta Temporada (Janeiro) ---
    r_temp = Reserva(hospede, quarto, 1, "site", date(2025, 1, 10), date(2025, 1, 11))
    valor_temp = r_temp.calcular_valor_total()
    print(f"\n3. Alta Temporada (Janeiro)")
    print(f"   Resultado: R$ {valor_temp:.2f}")

    # --- CASO 4: Com Adicionais ---
    r_adicional = Reserva(hospede, quarto, 1, "site", date(2025, 3, 10), date(2025, 3, 11))
    r_adicional.lancar_adicional("Coca-Cola", 10.00)
    valor_total = r_adicional.calcular_valor_total()
    print(f"\n4. Com Adicional (Esperado: 110.00)")
    print(f"   Resultado: R$ {valor_total:.2f}")

if __name__ == "__main__":
    testar_precos()