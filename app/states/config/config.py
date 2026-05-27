
import os
from dotenv import load_dotenv

load_dotenv()

USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE_SMTP")
SENHA_REMETENTE = os.getenv("SENHA_REMETENTE_SMTP")

DOMINIO_INSTITUICAO = os.getenv("DOMINIO_INSTITUICAO")

INT_FIELDS = ["Faltas", "Série"]
DEBUG = False
NOME_JSON = 'dados.json'
