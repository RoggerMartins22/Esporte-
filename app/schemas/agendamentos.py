from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from enum import Enum


class AgendamentoStatus(str, Enum):
    confirmado = "Confirmado"
    cancelado = "Cancelado"
    concluido = "Concluido"
    renovado = "Renovado"


class AgendamentoBase(BaseModel):
    id_quadra: int
    id_usuario: Optional[int] = None
    data: date
    horario_inicio: time
    horario_fim: time

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoDetalhadoResponse(BaseModel):
    id_agendamento: int
    nome_quadra: str
    nome_usuario: str
    id_usuario: Optional[int] = None
    data: date
    horario_inicio: time
    horario_fim: time
    status: AgendamentoStatus

class AgendamentoRenovarRequest(BaseModel):
        nova_data: date

class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int

    class Config:
        orm_mode = True