import reflex as rx
from sqlmodel import Field

class PerfilAcademico(rx.Model, table=True):
    ra: str = Field(unique=True)
    senha_criptografada: str = ""
    dados_json: str
