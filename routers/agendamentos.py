from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.auth import token_verifier
from database.database import get_db
from typing import List
from schemas.agendamentos import AgendamentoCreate, AgendamentoResponse
from services.agendamentos import AgendamentoService

router = APIRouter(
    prefix="/agendamentos", 
    tags=["Agendamentos"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/agendar-quadra")
async def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    return AgendamentoService.criar_agendamento(db=db, agendamento=agendamento)

"""
@router.get("/", response_model=List[AgendamentoResponse])
def listar_agendamentos():
    return agendamento_service.listar_agendamentos()
"""