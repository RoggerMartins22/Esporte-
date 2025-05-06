from sqlalchemy import Column, Integer, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from schemas.agendamentos import AgendamentoStatus

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id_agendamento = Column(Integer, primary_key=True, index=True)
    id_quadra = Column(Integer, ForeignKey("quadras.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    data = Column(Date, nullable=False)
    horario_inicio = Column(Time, nullable=False)
    horario_fim = Column(Time, nullable=False)

    status = Column(Enum(AgendamentoStatus), default=AgendamentoStatus.confirmado, nullable=False)

    quadra = relationship("quadras", back_populates="agendamentos")
    pessoa = relationship("users", back_populates="agendamentos")