import sys
import os
from datetime import datetime, date
from typing import List

# Importando nossos módulos
from roomex.models import Quarto, Hospede, Reserva
from roomex.dados import carregar_dados, salvar_dados
from roomex.reports import calcular_taxa_ocupacao

# --- Variáveis Globais (Estado do Sistema) ---
quartos: List[Quarto] = []
reservas: List[Reserva] = []
ARQUIVO_QUARTOS = "quartos.json"
ARQUIVO_RESERVAS = "reservas.json"

# --- Funções Auxiliares ---

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def salvar_tudo():
    """Salva o estado atual nos arquivos JSON."""
    salvar_dados(reservas, ARQUIVO_RESERVAS)
    # Quartos geralmente não mudam, mas se mudarmos status, precisaria salvar
    # salvar_dados(quartos, ARQUIVO_QUARTOS) 
    print("💾 Dados salvos automaticamente.")

def ler_data(mensagem: str) -> date:
    """Solicita uma data ao usuário e trata erros."""
    while True:
        entrada = input(f"{mensagem} (DD/MM/AAAA): ")
        try:
            return datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("❌ Formato inválido! Use dia/mês/ano (ex: 25/12/2025).")

def buscar_quarto(numero: int):
    for q in quartos:
        if q.numero == numero:
            return q
    return None

def buscar_reserva_por_quarto(numero_quarto: int):
    """Busca uma reserva ATIVA ou PENDENTE para o quarto informado."""
    for r in reservas:
        if r.quarto.numero == numero_quarto and r.status in ["PENDENTE", "ATIVA"]:
            return r
    return None

# --- Ações do Menu ---

def listar_quartos_disponiveis():
    print("\n--- Quartos Disponíveis ---")
    # Aqui poderíamos filtrar por data, mas vamos listar todos por simplicidade
    for q in quartos:
        print(f"Quarto {q.numero} ({q.tipo}) - Cap: {q.capacidade} - Diária: R$ {q.tarifa_base:.2f}")

def nova_reserva():
    print("\n--- 🆕 Nova Reserva ---")
    listar_quartos_disponiveis()
    
    try:
        num_quarto = int(input("Digite o número do quarto desejado: "))
        quarto = buscar_quarto(num_quarto)
        if not quarto:
            print("❌ Quarto não encontrado.")
            return

        # Dados do Hóspede
        print("\nDados do Hóspede:")
        nome = input("Nome completo: ")
        doc = input("Documento (CPF/RG): ")
        email = input("E-mail: ")
        tel = input("Telefone: ")
        hospede = Hospede(nome, doc, email, tel)

        # Dados da Reserva
        dt_ent = ler_data("Data de Entrada")
        dt_sai = ler_data("Data de Saída")
        qtd_pessoas = int(input("Quantidade de pessoas: "))

        # Criação
        nova = Reserva(hospede, quarto, qtd_pessoas, "Balcão", dt_ent, dt_sai)
        
        # Prévia do valor
        print(f"\nValor estimado: R$ {nova.calcular_valor_total():.2f}")
        confirmar = input("Confirmar reserva? (S/N): ").upper()
        
        if confirmar == 'S':
            reservas.append(nova)
            salvar_tudo()
            print("✅ Reserva criada com sucesso!")
        else:
            print("🚫 Operação cancelada.")

    except ValueError as e:
        print(f"❌ Erro nos dados: {e}")

def realizar_acoes_reserva(tipo_acao):
    """Função genérica para Check-in, Check-out e Lançamentos."""
    print(f"\n--- {tipo_acao} ---")
    try:
        num = int(input("Digite o número do quarto da reserva: "))
        reserva = buscar_reserva_por_quarto(num)
        
        if not reserva:
            print("❌ Nenhuma reserva Pendente ou Ativa encontrada neste quarto.")
            return

        print(f"Reserva encontrada: {reserva.hospede.nome} (Status: {reserva.status})")

        if tipo_acao == "Check-in":
            reserva.realizar_checkin()
            salvar_tudo()

        elif tipo_acao == "Check-out":
            print(f"Total a pagar: R$ {reserva.calcular_valor_total():.2f}")
            pagar = input("Registrar pagamento total agora? (S/N): ").upper()
            if pagar == 'S':
                reserva.adicionar_pagamento(reserva.calcular_valor_total(), "Dinheiro", date.today())
                reserva.realizar_checkout()
                salvar_tudo()

        elif tipo_acao == "Lançamentos":
            print("1. Adicionar Pagamento (Crédito)")
            print("2. Lançar Consumo/Serviço (Débito)")
            op = input("Opção: ")
            if op == '1':
                val = float(input("Valor: R$ "))
                forma = input("Forma (Pix/Cartão): ")
                reserva.adicionar_pagamento(val, forma, date.today())
            elif op == '2':
                desc = input("Descrição do item: ")
                val = float(input("Valor: R$ "))
                reserva.lancar_adicional(desc, val)
            salvar_tudo()
            
        elif tipo_acao == "Cancelar":
             confirmar = input("Tem certeza que deseja cancelar? (S/N): ").upper()
             if confirmar == 'S':
                 reserva.cancelar_reserva()
                 salvar_tudo()

    except ValueError as e:
        print(f"❌ Erro: {e}")

def menu_relatorios():
    print("\n--- 📊 Relatórios ---")
    dt_ini = ler_data("Data Início")
    dt_fim = ler_data("Data Fim")
    
    taxa = calcular_taxa_ocupacao(reservas, dt_ini, dt_fim, total_quartos=len(quartos))
    print(f"\nTaxa de Ocupação no período: {taxa}%")
    input("Pressione Enter para voltar...")

# --- Inicialização ---

def carregar_sistema():
    global quartos, reservas
    print("Carregando sistema...")
    quartos = carregar_dados(ARQUIVO_QUARTOS, Quarto)
    if not quartos:
        print("⚠️  Nenhum quarto encontrado! Rode o 'seed.py' primeiro.")
    
    # Passamos a lista de quartos para que as reservas possam se vincular a eles
    reservas = carregar_dados(ARQUIVO_RESERVAS, Reserva, quartos)
    print(f"Sistema carregado. {len(quartos)} quartos, {len(reservas)} reservas.")

def main():
    carregar_sistema()
    
    while True:
        print("\n" + "="*30)
        print("🏨 ROOMEX - Gestão Hoteleira")
        print("="*30)
        print("1. Nova Reserva")
        print("2. Fazer Check-in")
        print("3. Fazer Check-out")
        print("4. Registrar Consumo/Pagamento")
        print("5. Cancelar Reserva")
        print("6. Relatórios")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            nova_reserva()
        elif opcao == '2':
            realizar_acoes_reserva("Check-in")
        elif opcao == '3':
            realizar_acoes_reserva("Check-out")
        elif opcao == '4':
            realizar_acoes_reserva("Lançamentos")
        elif opcao == '5':
            realizar_acoes_reserva("Cancelar")
        elif opcao == '6':
            menu_relatorios()
        elif opcao == '0':
            print("Saindo... Até logo! 👋")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()