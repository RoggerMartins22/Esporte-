from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DisponivelEnum(str, Enum):
    S = "S"
    N = "N"

class QuadraBase(BaseModel):
    NOME_QUADRA: str
    ENDERECO: str
    ESPORTE: str
    DESCRICAO: Optional[str] = None
    DISPONIVEL: DisponivelEnum

    class Config:
        orm_mode = True

class QuadraCreate(QuadraBase):
    pass  

class Quadra(QuadraBase):
    ID: int

    class Config:
        orm_mode = True