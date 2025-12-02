from datetime import date
from typing import List
from roomex.models import Reserva

def calcular_taxa_ocupacao(reservas: List[Reserva], data_inicio: date, data_fim: date, total_quartos: int) -> float:
    """
    Calcula a taxa de ocupação (%) em um determinado período.
    
    Fórmula: (Dias Ocupados / (Total Quartos * Dias no Período)) * 100
    """
    if total_quartos <= 0:
        return 0.0

    # 1. Calcula quantos dias tem o período do relatório
    dias_no_periodo = (data_fim - data_inicio).days
    if dias_no_periodo <= 0:
        raise ValueError("A data final do relatório deve ser posterior à data inicial.")

    total_capacidade_dias = total_quartos * dias_no_periodo
    dias_ocupados = 0

    # 2. Percorre as reservas para somar os dias ocupados DENTRO do período
    for reserva in reservas:
        # Apenas se a reserva estiver CONFIRMADA ou CHECKIN/OUT (ignoramos canceladas/pendentes)
        # Nota: Como ainda não implementamos a lógica de confirmação, vamos considerar todas
        # exceto as explicitamente canceladas, se houver.
        if reserva.status == "CANCELADA":
            continue

        # Lógica de Interseção de Datas:
        # Descobre quando a ocupação começa (o que for maior: entrada da reserva ou inicio do relatorio)
        inicio_efetivo = max(reserva.data_entrada, data_inicio)
        # Descobre quando a ocupação termina (o que for menor: saida da reserva ou fim do relatorio)
        fim_efetivo = min(reserva.data_saida, data_fim)

        # Se houver dias válidos nessa interseção, soma
        if inicio_efetivo < fim_efetivo:
            dias = (fim_efetivo - inicio_efetivo).days
            dias_ocupados += dias

    # 3. Calcula a porcentagem final
    taxa = (dias_ocupados / total_capacidade_dias) * 100
    
    return round(taxa, 2)