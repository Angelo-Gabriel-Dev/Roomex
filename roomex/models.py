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

    def __str__(self) -> str:
        return f"{self.nome} (Doc: {self.documento})"


class Quarto:
    """
    Representa um quarto do hotel.
    """
    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float):
        self.numero = numero
        self.tipo = tipo
        # Usamos os setters aqui para garantir a validação desde a criação
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        
        self.status: str = "DISPONIVEL"
        self.reservas: List['Reserva'] = []

    # --- Encapsulamento e Validações (Semana 2) ---

    @property
    def capacidade(self) -> int:
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor: int):
        if valor < 1:
            raise ValueError("A capacidade deve ser de pelo menos 1 pessoa.")
        self._capacidade = valor

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        if valor <= 0:
            raise ValueError("A tarifa base deve ser maior que zero.")
        self._tarifa_base = valor

    # --- Métodos Especiais (Semana 2) ---

    def __str__(self) -> str:
        """Retorna uma representação legível do quarto."""
        return f"Quarto {self.numero} ({self.tipo}) - Cap: {self.capacidade} - R$ {self.tarifa_base:.2f}"

    def __lt__(self, other: 'Quarto') -> bool:
        """Permite ordenar quartos (pelo número)."""
        return self.numero < other.numero


class Reserva:
    """
    Representa uma reserva de quarto feita por um hóspede.
    """
    def __init__(self, hospede: Hospede, quarto: Quarto, num_hospedes: int, 
                 origem: str, data_entrada: date, data_saida: date):
        
        self.hospede = hospede
        self.quarto = quarto
        self.origem = origem
        self.status: str = "PENDENTE"
        
        # Inicializa variáveis internas para permitir a validação nos setters
        self._data_entrada = data_entrada
        self._data_saida = data_saida
        
        # Validação via setters
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.num_hospedes = num_hospedes

        self.pagamentos: List['Pagamento'] = []
        self.adicionais: List['Adicional'] = []

    # --- Encapsulamento e Validações (Semana 2) ---

    @property
    def num_hospedes(self) -> int:
        return self._num_hospedes

    @num_hospedes.setter
    def num_hospedes(self, valor: int):
        # Valida se o número de hóspedes cabe no quarto selecionado
        if valor > self.quarto.capacidade:
            raise ValueError(f"O quarto {self.quarto.numero} suporta apenas {self.quarto.capacidade} pessoas.")
        self._num_hospedes = valor

    @property
    def data_entrada(self) -> date:
        return self._data_entrada
    
    @data_entrada.setter
    def data_entrada(self, nova_data: date):
        # Se data_saida já existir, valida se entrada é anterior
        if hasattr(self, '_data_saida') and self._data_saida and nova_data >= self._data_saida:
             raise ValueError("A data de entrada deve ser anterior à data de saída.")
        self._data_entrada = nova_data

    @property
    def data_saida(self) -> date:
        return self._data_saida

    @data_saida.setter
    def data_saida(self, nova_data: date):
        # Valida se saída é posterior à entrada
        if nova_data <= self._data_entrada:
            raise ValueError("A data de saída deve ser posterior à data de entrada.")
        self._data_saida = nova_data

    # --- Métodos Especiais (Semana 2) ---

    def __len__(self) -> int:
        """Retorna o número de diárias da reserva."""
        delta = self.data_saida - self.data_entrada
        return delta.days

    def __eq__(self, other: object) -> bool:
        """Verifica se duas reservas são iguais (mesmo quarto e mesmo intervalo)."""
        if not isinstance(other, Reserva):
            return NotImplemented
        return (self.quarto.numero == other.quarto.numero and
                self.data_entrada == other.data_entrada and
                self.data_saida == other.data_saida)

    def __str__(self) -> str:
        return f"Reserva no {self.quarto.numero} para {self.hospede.nome} ({self.__len__()} noites)"


class Pagamento:
    """
    Representa um pagamento (crédito) associado a uma reserva.
    """
    def __init__(self, data: date, forma: str, valor: float):
        self.data = data
        self.forma = forma
        self.valor = valor


class Adicional:
    """
    Representa um item de consumo ou serviço extra (débito)
    associado a uma reserva.
    """
    def __init__(self, descricao: str, valor: float):
        self.descricao = descricao
        self.valor = valor