from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class PerfilAcademico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ra: str = Field(unique=True)
    senha_criptografada: str = ""
    dados_json: str

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    autor_ra: str = Field(index=True)
    autor_nome: str
    texto: str
    imagem_url: Optional[str] = None
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
