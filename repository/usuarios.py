from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuarios import User
from schemas.usuarios import UserCreate, ResetPasswordRequest

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
    
    @staticmethod
    def update_user_password(db: Session, user: ResetPasswordRequest):

        db_user = UserRepository.get_user_by_email(db, email=user.email)

        try:
            db_user.senha = user.nova_senha
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_usuario_by_id(db: Session, usuario_id: int):
        return db.query(User).filter(User.id == usuario_id).first()
    