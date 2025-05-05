from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from schemas.usuarios import StatusEnum, PermissaoEnum

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.A, nullable=False)
    permissao = Column(SQLEnum(PermissaoEnum), default=PermissaoEnum.USER, nullable=False)
    data_cadastro = Column(DateTime, default=lambda: datetime.now() - timedelta(hours=3))