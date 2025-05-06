from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.agendamentos import Agendamento
from schemas.agendamentos import AgendamentoCreate


class AgendamentoRepository:

    @staticmethod
    def create_agendamento_repository(db: Session, agendamento: AgendamentoCreate):

        db_agendamento = Agendamento(
            id_quadra=agendamento.id_quadra,
            id_usuario=agendamento.id_usuario,
            data=agendamento.data,
            horario_inicio=agendamento.horario_inicio,
            horario_fim=agendamento.horario_fim
        )

        try:
            db.add(db_agendamento)
            db.commit()
            db.refresh(db_agendamento)
            return db_agendamento
        except IntegrityError as e:
            db.rollback()
            raise e
        
    @staticmethod
    def get_agendamento_by_data_hora(db: Session, agendamento):
        return db.query(Agendamento).filter(
            Agendamento.data == agendamento.data,
            Agendamento.horario_inicio <= agendamento.horario_inicio,
            Agendamento.horario_fim >= agendamento.horario_fim,
            Agendamento.id_quadra == agendamento.id_quadra
        ).first()