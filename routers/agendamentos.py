from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.auth import token_verifier
from database.database import get_db
from schemas.agendamentos import AgendamentoCreate
from services.agendamentos import AgendamentoService

router = APIRouter(
    prefix="/agendamentos", 
    tags=["Agendamentos"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/agendar-quadra")
async def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    return AgendamentoService.criar_agendamento(db=db, agendamento=agendamento)

@router.get("/")
def listar_agendamentos(db: Session = Depends(get_db)):
    return AgendamentoService.listar_agendamentos(db=db)

@router.get("/quadra/{id_quadra}")
def listar_agendamentos_por_id_quadra(id_quadra: int, db: Session = Depends(get_db)):
    return AgendamentoService.listar_agendamentos_por_id_quadra(db=db, id_quadra=id_quadra)

@router.get("/usuario/{id_usuario}")
def listar_agendamentos_por_id_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return AgendamentoService.listar_agendamentos_por_id_usuario(db=db, id_usuario=id_usuario)