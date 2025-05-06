from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from repository.usuarios import UserRepository
from auth.hashing import AuthHandler
from auth.auth import OAuth2
from schemas.usuarios import UserCreate, LoginRequest, ResetPasswordRequest
import re


def validate_user_info(user):
    
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", user.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome inválido. Deve conter apenas letras."
        )

    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido."
        )
    
    if not re.match(r"^\d{11}$", user.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido. Deve conter exatamente 11 números, sem pontos ou traços."
        )
    
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", user.senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Senha inválida. A senha deve ter no mínimo 8 caracteres, "
                "incluir pelo menos 1 letra maiúscula, 1 letra minúscula e 1 número."
            )
        )
    

def create_user_service(db: Session, user: UserCreate):

    validate_user_info(user)

    user.senha = AuthHandler.hash_password(user.senha)
            
    if UserRepository.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este e-mail cadastrado."
        )

    if UserRepository.get_user_by_cpf(db, user.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este CPF cadastrado."
        )

    try:
        result = UserRepository.create_user_repository(db=db, user=user)
        if result:
            return {
                "status_code": status.HTTP_201_CREATED,
                "detail": "Usuário cadastrado com sucesso!"
            }

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e) 
        )

        
def login_user_service(db: Session, user: LoginRequest):
    user_db = UserRepository.get_user_by_cpf(db=db, cpf=user.cpf)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorreta!"
        )
    
    if not AuthHandler.verify_password(user.senha, user_db.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorreta!"
        )
    
    return OAuth2.user_login(user_db)
                

def reset_password_service(db: Session, user: ResetPasswordRequest):

    user_db = UserRepository.get_user_by_cpf(db=db, cpf=user.cpf)
                                               
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado!"
        )

    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", user.nova_senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Senha inválida. A senha deve ter no mínimo 8 caracteres, "
                "incluir pelo menos 1 letra maiúscula, 1 letra minúscula e 1 número."
            )
        )
    
    user.nova_senha = AuthHandler.hash_password(user.nova_senha)

    try:
        UserRepository.update_user_password(db=db, user=user)
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "Senha redefinida com sucesso!"
        }
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )