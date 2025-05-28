from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class Esporte(Base):
    __tablename__ = 'esportes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False)

    quadras = relationship("Quadra", back_populates="esporte_info")
