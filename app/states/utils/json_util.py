import json

def extrai_json(nome_arquivo: str):
    ## abre json com os dados
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados

def salvar_json(materias, aluno):
    with open("dados.json", "w", encoding="utf-8") as arquivo:
        dados = {   ## formata json com campos separados: 'aluno' e 'disciplinas'
            "aluno": aluno,
            "disciplinas": materias
        }
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)