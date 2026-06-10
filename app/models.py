from typing import Optional
from sqlmodel import Field, SQLModel
from reflex.model import ModelRegistry


class PerfilAcademico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ra: str = Field(unique=True)
    senha_criptografada: str = ""
    dados_json: str


# Registra o modelo no Reflex para que as migrations (reflex db migrate) funcionem
ModelRegistry.register(PerfilAcademico)
