# Roomex

Este projeto é um sistema de linha de comando (CLI) para gerenciamento de reservas de hotel, desenvolvido como Projeto 1 da disciplina de Programação Orientada a Objetos (POO) do curso de Engenharia de Software da UFCA.

## 🎯 Objetivo

O objetivo principal é aplicar os conceitos fundamentais de POO (herança, encapsulamento, polimorfismo e composição) para criar um sistema funcional que gerencie hóspedes, quartos, reservas, check-in/check-out e relatórios básicos.

## 🏛️ Estrutura Planejada de Classes

A modelagem inicial planejada para o sistema é:

* **Pessoa** (Classe base)
    * **Hospede** (Herda de Pessoa)
* **Quarto** (Classe base)
    * **QuartoSimples** (Herda de Quarto)
    * **QuartoDuplo** (Herda de Quarto)
    * **QuartoLuxo** (Herda de Quarto)
* **Reserva** (Agrega Hóspede e Quarto; Compõe Pagamento e Adicional)
* **Pagamento**
* **Adicional**
* **Hotel** (Classe principal para orquestrar as operações)
