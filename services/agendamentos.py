from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from repository.quadras import QuadrantRepository
from repository.usuarios import UserRepository
from repository.agendamentos import AgendamentoRepository


class AgendamentoService:

    def validate_agendamento_info(db, agendamento):

        if not QuadrantRepository.get_quadrant_by_id(db, agendamento.id_quadra):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadra não encontrada."
            )
        
        if not UserRepository.get_usuario_by_id(db, agendamento.id_usuario):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        if AgendamentoRepository.get_agendamento_by_data_hora(db, agendamento):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um agendamento para essa quadra nesse horário."
            )  
        
        if agendamento.horario_inicio.hour < 8 or agendamento.horario_fim.hour > 22:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Horário inválido. O agendamento deve ser entre 08:00 e 22:00."
            ) 

    @staticmethod
    def criar_agendamento(db: Session, agendamento): 
        
        AgendamentoService.validate_agendamento_info(db, agendamento)

        try:
            result = AgendamentoRepository.create_agendamento_repository(db=db, agendamento=agendamento)
            if result:
                return {
                    "status_code": status.HTTP_201_CREATED,
                    "detail": "Agendamento criado com sucesso!",
                    "Agendamento": result
                }
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e) 
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar agendamento: " + str(e)
            )