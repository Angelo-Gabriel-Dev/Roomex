from datetime import date
from typing import List, Optional

class Hospede:
    """
    Representa um hóspede cadastrado no sistema.
    """
    def __init__(self, nome: str, documento: str, email: str, telefone: str):
        self.nome = nome
        self.documento = documento
        self.email = email
        self.telefone = telefone
        self.historico_reservas: List['Reserva'] = []

    pass


class Quarto:
    """
    Representa um quarto do hotel.
    """
    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        self.status: str = "DISPONIVEL"
        self.reservas: List['Reserva'] = []

    pass


class Reserva:
    """
    Representa uma reserva de quarto feita por um hóspede.
    """
    def __init__(self, hospede: Hospede, quarto: Quarto, num_hospedes: int, 
                 origem: str, data_entrada: date, data_saida: date):
        
        # Relacionamentos de Agregação
        self.hospede = hospede
        self.quarto = quarto
        
        # Atributos da Reserva
        self.num_hospedes = num_hospedes
        self.origem = origem
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.status: str = "PENDENTE"

        # Relacionamentos de Composição
        self.pagamentos: List['Pagamento'] = []
        self.adicionais: List['Adicional'] = []

    pass


class Pagamento:
    """
    Representa um pagamento (crédito) associado a uma reserva.
    """
    def __init__(self, data: date, forma: str, valor: float):
        self.data = data
        self.forma = forma
        self.valor = valor

    pass


class Adicional:
    """
    Representa um item de consumo ou serviço extra (débito)
    associado a uma reserva.
    """
    def __init__(self, descricao: str, valor: float):
        self.descricao = descricao
        self.valor = valor

    pass