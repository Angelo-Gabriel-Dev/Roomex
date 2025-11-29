from datetime import date
from typing import List, Optional

class Pessoa:
    """Classe base que representa uma pessoa no sistema (Hóspede, Funcionário, etc.)."""
    def __init__(self, nome: str, documento: str, email: str, telefone: str):
        self.nome = nome
        self.documento = documento
        self.email = email
        self.telefone = telefone

    def __str__(self) -> str:
        return f"{self.nome} (Doc: {self.documento})"


class Hospede(Pessoa):
    """Representa um hóspede do hotel, que é um tipo de Pessoa."""
    def __init__(self, nome: str, documento: str, email: str, telefone: str):
        super().__init__(nome, documento, email, telefone)
        self.historico_reservas: List['Reserva'] = []
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "documento": self.documento,
            "email": self.email,
            "telefone": self.telefone
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            nome=dados["nome"],
            documento=dados["documento"],
            email=dados["email"],
            telefone=dados["telefone"]
        )

class Quarto:
    """Representa um quarto físico do hotel com suas características e tarifa."""
    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        self.status: str = "DISPONIVEL"
        self.reservas: List['Reserva'] = []

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

    def __str__(self) -> str:
        return f"Quarto {self.numero} ({self.tipo}) - Cap: {self.capacidade} - R$ {self.tarifa_base:.2f}"

    def __lt__(self, other: 'Quarto') -> bool:
        return self.numero < other.numero
    
    def to_dict(self):
        return {
            "numero": self.numero,
            "tipo": self.tipo,
            "capacidade": self.capacidade,
            "tarifa_base": self.tarifa_base,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, dados):
        quarto = cls(
            numero=dados["numero"],
            tipo=dados["tipo"],
            capacidade=dados["capacidade"],
            tarifa_base=dados["tarifa_base"]
        )
        quarto.status = dados["status"]
        return quarto

class Reserva:
    """Representa uma reserva de um quarto feita por um hóspede para um período."""
    def __init__(self, hospede: Hospede, quarto: Quarto, num_hospedes: int, 
                 origem: str, data_entrada: date, data_saida: date):
        self.hospede = hospede
        self.quarto = quarto
        self.origem = origem
        self.status: str = "PENDENTE"
        self._data_entrada = data_entrada
        self._data_saida = data_saida
        
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.num_hospedes = num_hospedes

        self.pagamentos: List['Pagamento'] = []
        self.adicionais: List['Adicional'] = []
    
    def adicionar_pagamento(self, valor: float, forma: str, data_pagamento: date):
        novo_pagamento = Pagamento(data_pagamento, forma, valor)

        self.pagamentos.append(novo_pagamento)
        print(f"Pagamento de R$ {valor:.2f} ({forma}) registrado com sucesso.")
    
    def lancar_adicional(self, descricao: str, valor: float):
        novo_adicional = Adicional(descricao, valor)
        self.adicionais.append(novo_adicional)
        print(f"Adicional '{descricao}' de R$ {valor:.2f} lançado com sucesso.")

    @property
    def num_hospedes(self) -> int:
        return self._num_hospedes

    @num_hospedes.setter
    def num_hospedes(self, valor: int):
        if valor > self.quarto.capacidade:
            raise ValueError(f"O quarto {self.quarto.numero} suporta apenas {self.quarto.capacidade} pessoas.")
        self._num_hospedes = valor

    @property
    def data_entrada(self) -> date:
        return self._data_entrada
    
    @data_entrada.setter
    def data_entrada(self, nova_data: date):
        if hasattr(self, '_data_saida') and self._data_saida and nova_data >= self._data_saida:
             raise ValueError("A data de entrada deve ser anterior à data de saída.")
        self._data_entrada = nova_data

    @property
    def data_saida(self) -> date:
        return self._data_saida

    @data_saida.setter
    def data_saida(self, nova_data: date):
        if nova_data <= self._data_entrada:
            raise ValueError("A data de saída deve ser posterior à data de entrada.")
        self._data_saida = nova_data

    def __len__(self) -> int:
        delta = self.data_saida - self.data_entrada
        return delta.days

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reserva):
            return NotImplemented
        return (self.quarto.numero == other.quarto.numero and
                self.data_entrada == other.data_entrada and
                self.data_saida == other.data_saida)

    def __str__(self) -> str:
        return f"Reserva no {self.quarto.numero} para {self.hospede.nome} ({self.__len__()} noites)"
    
    def to_dict(self):
        return {
            "hospede": self.hospede.to_dict(), # Chama o to_dict do Hospede
            "quarto_numero": self.quarto.numero, # Salvamos só o número do quarto para buscar depois
            "num_hospedes": self.num_hospedes,
            "origem": self.origem,
            "data_entrada": self.data_entrada.isoformat(),
            "data_saida": self.data_saida.isoformat(),
            "status": self.status,
            "pagamentos": [p.to_dict() for p in self.pagamentos], # Lista de dicts
            "adicionais": [a.to_dict() for a in self.adicionais]  # Lista de dicts
        }

    @classmethod
    def from_dict(cls, dados, lista_quartos):
        # Para recriar a reserva, precisamos achar o objeto Quarto real na lista de quartos do sistema
        quarto_real = next((q for q in lista_quartos if q.numero == dados["quarto_numero"]), None)
        
        if not quarto_real:
            raise ValueError(f"Quarto {dados['quarto_numero']} não encontrado.")

        hospede = Hospede.from_dict(dados["hospede"])
        
        reserva = cls(
            hospede=hospede,
            quarto=quarto_real,
            num_hospedes=dados["num_hospedes"],
            origem=dados["origem"],
            data_entrada=date.fromisoformat(dados["data_entrada"]),
            data_saida=date.fromisoformat(dados["data_saida"])
        )
        reserva.status = dados["status"]
        
        # Recria as listas de pagamentos e adicionais
        reserva.pagamentos = [Pagamento.from_dict(p) for p in dados["pagamentos"]]
        reserva.adicionais = [Adicional.from_dict(a) for a in dados["adicionais"]]
        
        return reserva

class Pagamento:
    """Representa um registro financeiro de crédito (pagamento) na reserva."""
    def __init__(self, data: date, forma: str, valor: float):
        self.data = data
        self.forma = forma
        self.valor = valor

    def to_dict(self) -> dict:
        return {
            "data": self.data.isoformat(),
            "forma": self.forma,
            "valor": self.valor
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Pagamento':
        return cls(
            data=date.fromisoformat(data["data"]),
            forma=data["forma"],
            valor=data["valor"]
        )

class Adicional:
    """Representa um registro financeiro de débito (consumo/serviço extra) na reserva."""
    def __init__(self, descricao: str, valor: float):
        self.descricao = descricao
        self.valor = valor
    
    def to_dict(self) -> dict:
        return {
            "descricao": self.descricao,
            "valor": self.valor
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Adicional':
        return cls(
            descricao=data["descricao"],
            valor=data["valor"]
        )