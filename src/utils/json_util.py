import json

def extrai_json(nome_arquivo: str):
    ## abre json com os dados
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados