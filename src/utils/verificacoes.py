from src.config import (
    USUARIO,
    DOMINIO_INSTITUICAO,
    EMAIL_REMETENTE,
    SENHA_REMETENTE,
    NOME_JSON
)
from src.utils.json_util import extrai_json
from src.services.email_service import alerta_faltas

def verifica_faltas():
    dados = extrai_json(NOME_JSON)

    for disciplina in dados['disciplinas']:
        faltas = disciplina['Faltas']

        if faltas >= 8:
            alerta_faltas(disciplina)