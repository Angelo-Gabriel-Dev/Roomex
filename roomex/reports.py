from datetime import date
from typing import List, Dict
from roomex.models import Reserva

def _interseccao_dias(reserva: Reserva, data_inicio: date, data_fim: date) -> int:
    """
    Retorna quantos dias da reserva caem dentro do período do relatório.
    """
    inicio_efetivo = max(reserva.data_entrada, data_inicio)
    fim_efetivo = min(reserva.data_saida, data_fim)
    
    if inicio_efetivo < fim_efetivo:
        return (fim_efetivo - inicio_efetivo).days
    return 0

def calcular_metricas_financeiras(reservas: List[Reserva], data_inicio: date, data_fim: date, total_quartos: int) -> Dict[str, float]:
    """
    Gera um dicionário com Taxa de Ocupação, ADR e RevPAR.
    Fórmulas baseadas no documento de requisitos.
    """
    if total_quartos <= 0:
        return {"ocupacao": 0.0, "adr": 0.0, "revpar": 0.0, "receita_total": 0.0}

    # Dias totais do período do relatório
    dias_no_periodo = (data_fim - data_inicio).days
    if dias_no_periodo <= 0:
        # Evita divisão por zero ou data inválida
        return {"ocupacao": 0.0, "adr": 0.0, "revpar": 0.0, "receita_total": 0.0}

    total_dias_disponiveis_hotel = total_quartos * dias_no_periodo
    dias_ocupados_total = 0
    receita_periodo = 0.0

    for reserva in reservas:
        # Ignora canceladas e no-show para cálculo de receita e ocupação efetiva
        if reserva.status in ["CANCELADA", "NO_SHOW", "PENDENTE"]:
            continue

        dias_interseccao = _interseccao_dias(reserva, data_inicio, data_fim)
        
        if dias_interseccao > 0:
            dias_ocupados_total += dias_interseccao
            
            # Cálculo de Receita Proporcional:
            # Se a reserva custa R$ 1000 por 5 dias, mas só 2 dias caem neste relatório,
            # somamos apenas R$ 400 (2 * média diária) ao relatório.
            valor_total = reserva.calcular_valor_total()
            dias_totais_reserva = len(reserva)
            
            if dias_totais_reserva > 0:
                receita_diaria_media = valor_total / dias_totais_reserva
                receita_periodo += (receita_diaria_media * dias_interseccao)

    # 1. Taxa de Ocupação (%)
    taxa_ocupacao = (dias_ocupados_total / total_dias_disponiveis_hotel) * 100

    # 2. ADR (Average Daily Rate) = Receita Total / Diárias Vendidas
    adr = receita_periodo / dias_ocupados_total if dias_ocupados_total > 0 else 0.0

    # 3. RevPAR (Revenue per Available Room) = Receita Total / Total de Quartos Disponíveis (Inventário)
    revpar = receita_periodo / total_dias_disponiveis_hotel

    return {
        "ocupacao": round(taxa_ocupacao, 2),
        "adr": round(adr, 2),
        "revpar": round(revpar, 2),
        "receita_total": round(receita_periodo, 2)
    }

def relatorio_cancelamentos(reservas: List[Reserva], data_inicio: date, data_fim: date) -> Dict[str, int]:
    """
    Conta cancelamentos e No-Shows que ocorreriam dentro do período.
    """
    stats = {"CANCELADA": 0, "NO_SHOW": 0, "TOTAL": 0}
    
    for reserva in reservas:
        # Verifica se a reserva tem interseção com o período
        if _interseccao_dias(reserva, data_inicio, data_fim) > 0 or (data_inicio <= reserva.data_entrada <= data_fim):
            if reserva.status == "CANCELADA":
                stats["CANCELADA"] += 1
            elif reserva.status == "NO_SHOW":
                stats["NO_SHOW"] += 1
    
    stats["TOTAL"] = stats["CANCELADA"] + stats["NO_SHOW"]
    return stats