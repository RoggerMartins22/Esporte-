from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.usuarios import (create_user_service, login_user_service, enviar_email_redefinicao_senha, redefinir_senha_com_token, consulta_info_usuarios)
from schemas.usuarios import UserCreate, LoginRequest, ResetPasswordRequest, ValidatrPasswordRequest
from auth.auth import token_verifier, get_current_user_id
from database.database import get_db


routerUser = APIRouter(
    prefix="/usuario-info",
    tags=["user-info"],
    dependencies=[Depends(token_verifier)]
)

router = APIRouter(
    prefix="/usuario",
    tags=["users"],
)

@router.post("/cadastrar")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db=db, user=user)

@router.post("/login")
async def login_user(request_form_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = LoginRequest(
        cpf=request_form_user.username,
        senha=request_form_user.password
    )

    return login_user_service(db=db, user=user)

@router.post("/redefinir-senha")
async def solicitar_redefinicao_senha(user: ResetPasswordRequest, db: Session = Depends(get_db)):
    return enviar_email_redefinicao_senha(db=db, user=user)

@router.post("/validar-nova-senha/{token}")
async def confirmar_nova_senha(user: ValidatrPasswordRequest, db: Session = Depends(get_db)):
    return redefinir_senha_com_token(db=db, user=user)

@routerUser.get("/")
async def consulta_dados_usuarios(db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return consulta_info_usuarios(db=db,  user_id=user_id)