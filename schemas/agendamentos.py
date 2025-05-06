from pydantic import BaseModel
from datetime import date, time
from enum import Enum


class AgendamentoStatus(str, Enum):
    confirmado = "Confirmado"
    cancelado = "Cancelado"
    concluido = "Concluido"


class AgendamentoBase(BaseModel):
    id_quadra: int
    id_pessoa: int
    data: date
    horario_inicio: time
    horario_fim: time

class AgendamentoCreate(AgendamentoBase):
    pass


class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int

    class Config:
        orm_mode = True