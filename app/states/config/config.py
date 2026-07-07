
import os
from dotenv import load_dotenv, set_key

load_dotenv()

USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE_SMTP")
SENHA_REMETENTE = os.getenv("SENHA_REMETENTE_SMTP")

DOMINIO_INSTITUICAO = os.getenv("DOMINIO_INSTITUICAO")

INT_FIELDS = ["Faltas", "Série"]
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
NOME_JSON = 'dados.json'

ENV_PATH = os.path.join(os.path.dirname(__file__), "../../../../.env")

def salvar_credenciais(usuario: str, senha: str):
    """Salva as credenciais do usuário no arquivo .env e atualiza as variáveis globais."""
    global USUARIO, SENHA
    set_key(ENV_PATH, "USUARIO", usuario)
    set_key(ENV_PATH, "SENHA", senha)
    USUARIO = usuario
    SENHA = senha
