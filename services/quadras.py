from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from schemas.quadras import QuadraCreate
from repository.quadras import QuadrantRepository
from repository.usuarios import UserRepository
import re


def validate_quadrant_info(quadra):
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", quadra.nome_quadra):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome da quadra inválido. Deve conter apenas letras."
        )

    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", quadra.esporte):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esporte inválido. Deve conter apenas letras."
        )


def create_quadrant_service(db: Session, quadra: QuadraCreate, user_id: int):

    user = UserRepository.get_role_user(db=db, id_usuario=user_id)
    
    if user.permissao == "USER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não permissão para acessar este menu!"
        )
    
    if QuadrantRepository.get_quadrant_by_name(db, quadra.nome_quadra):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma quadra com esse nome."
        )

    if QuadrantRepository.get_quadrant_by_address(db, quadra.endereco):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma quadra cadastrada nesse endereço."
        )
    
    try:
       
        result = QuadrantRepository.create_quadrant_repository(db=db, quadra=quadra)

        if result:
            return {
                "status_code": status.HTTP_201_CREATED,
                "detail": "Quadra cadastrada com sucesso!"
            }

    except HTTPException:
            raise
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e) 
        )