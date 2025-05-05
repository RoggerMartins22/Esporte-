from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuarios import User
from schemas.usuarios import UserCreate

class UserRepository:
    @staticmethod
    def create_user_repository(db: Session, user: UserCreate):
        db_user = User(email=user.email, cpf=user.cpf, nome=user.nome, senha=user.senha)
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            raise e
        
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_cpf(db: Session, cpf: str):
        return db.query(User).filter(User.cpf == cpf).first()