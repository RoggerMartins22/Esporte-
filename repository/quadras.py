from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.quadras import Quadra
from schemas.quadras import QuadraCreate

class QuadrantRepository:
    @staticmethod
    def create_quadrant_repository(db: Session, quadra: QuadraCreate):
        db_quadrant= Quadra(nome_quadra=quadra.nome_quadra, endereco=quadra.endereco, esporte=quadra.esporte, descricao=quadra.descricao)

        try:
            db.add(db_quadrant)
            db.commit()
            db.refresh(db_quadrant)
            return db_quadrant
        except IntegrityError as e:
            db.rollback()
            raise e

    @staticmethod   
    def get_quadrant_by_name(db: Session, nome_quadra: str):
        return db.query(Quadra).filter(Quadra.nome_quadra == nome_quadra).first()
    
    @staticmethod 
    def get_quadrant_by_address(db: Session, endereco: str):
        return db.query(Quadra).filter(Quadra.endereco == endereco).first()
    
    @staticmethod 
    def get_quadrant_by_id(db: Session, quadra_id: int):
        return db.query(Quadra).filter(Quadra.id == quadra_id).first()