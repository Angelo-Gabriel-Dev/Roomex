import json
import os
from typing import List, Type, Any

def salvar_dados(lista_objetos: List[Any], nome_arquivo: str):
    """
    Salva uma lista de objetos em um arquivo JSON.
    """
    # 1. Converte cada objeto da lista em dicionário
    lista_dicts = [obj.to_dict() for obj in lista_objetos]
    
    # 2. Abre o arquivo e grava
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(lista_dicts, arquivo, indent=4, ensure_ascii=False)
    
    print(f"Dados salvos com sucesso em {nome_arquivo}")

def carregar_dados(nome_arquivo: str, classe_tipo: Type, lista_quartos: List = None) -> List[Any]:
    """
    Carrega dados de um JSON e converte de volta para objetos.
    
    Args:
        nome_arquivo: Caminho do arquivo JSON.
        classe_tipo: A Classe que deve ser recriada (ex: Quarto, Hospede).
        lista_quartos: (Apenas para Reservas) Lista de quartos existentes para vincular.
    """
    if not os.path.exists(nome_arquivo):
        return []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        lista_dicts = json.load(arquivo)
    
    objetos = []
    for dados in lista_dicts:
        # Se for Reserva, precisa passar a lista de quartos
        if classe_tipo.__name__ == "Reserva":
            obj = classe_tipo.from_dict(dados, lista_quartos)
        else:
            obj = classe_tipo.from_dict(dados)
        objetos.append(obj)
        
    return objetos