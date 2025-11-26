# Roomex

Este projeto é um sistema de linha de comando (CLI) para gerenciamento de reservas de hotel, desenvolvido como Projeto 1 da disciplina de Programação Orientada a Objetos (POO) do curso de Engenharia de Software da UFCA.

## 🎯 Objetivo

O objetivo principal é aplicar os conceitos fundamentais de POO (herança, encapsulamento, polimorfismo e composição) para criar um sistema funcional que gerencie hóspedes, quartos, reservas, check-in/check-out e relatórios básicos.

## 🏛️ UML Textual (Diagrama de Classes)

Abaixo está o diagrama de classes planejado para o sistema, escrito em sintaxe Mermaid, agora incluindo a herança da classe base Pessoa.

```mermaid
classDiagram
    class Pessoa {
        -nome: str
        -documento: str
        -email: str
        -telefone: str
    }

    class Quarto {
        -numero: int
        -tipo: str
        -capacidade: int
        -tarifa_base: float
        -status: str
        +bloquear(motivo, período) void
        +verificar_disponibilidade(checkin, checkout) bool
    }

    class Hospede{
        +consultar_historico() list
    }

    class Reserva {
        -num_hospedes: int
        -origem: str
        -data_entrada: date
        -data_saida: date
        -status: str
        +calcular_valor_total() float
        +checkin() void
        +checkout() void
        +cancelar() void
    }

    class Pagamento {
        -data: date
        -forma: str
        -valor: float
    }

    class Adicional {
        -descricao: str
        -valor: float
    }

    %% Relacionamentos de Herança
    Pessoa <|-- Hospede

    %% Relacionamentos de Agregação e Composição
    Reserva o-- Hospede
    Reserva o-- Quarto
    Reserva *-- Pagamento
    Reserva *-- Adicional