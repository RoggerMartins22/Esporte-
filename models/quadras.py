from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database.base import Base
from schemas.quadras import DisponivelEnum

class Quadra(Base):
    __tablename__ = 'quadras'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_quadra = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    esporte = Column(Integer, ForeignKey("esportes.id"), nullable=False)
    descricao = Column(String, nullable=True)
    disponibilidade = Column(SQLEnum(DisponivelEnum), default=DisponivelEnum.S,nullable=False)

    agendamentos = relationship("Agendamento", back_populates="quadras")
    esportes = relationship("Esportes", back_populates="quadras")

