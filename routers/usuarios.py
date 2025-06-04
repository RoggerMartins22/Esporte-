from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.usuarios import UserService
from schemas.usuarios import UserCreate, LoginRequest, ResetPasswordRequest, ValidatePasswordRequest, NomeUpdate, EmailUpdate
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
    return UserService.create_user_service(db=db, user=user)

@router.post("/login")
async def login_user(request_form_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = LoginRequest(
        cpf=request_form_user.username,
        senha=request_form_user.password
    )

    return UserService.login_user_service(db=db, user=user)

@router.post("/redefinir-senha")
async def solicitar_redefinicao_senha(user: ResetPasswordRequest, db: Session = Depends(get_db)):
    return UserService.enviar_email_redefinicao_senha(db=db, user=user)

@router.post("/validar-nova-senha/{token}")
async def confirmar_nova_senha(token: str, nova_senha: ValidatePasswordRequest, db: Session = Depends(get_db)):
    return UserService.redefinir_senha_com_token(db=db, token=token, nova_senha=nova_senha)

@routerUser.get("/")
async def consulta_dados_usuarios(db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return UserService.consulta_info_usuarios(db=db, user_id=user_id)

@routerUser.post("/alterar-nome")
async def alterar_nome_usuario(nome: NomeUpdate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return UserService.update_nome_usuario(db=db, nome=nome, user_id=user_id)

@routerUser.post("/alterar-email")
async def alterar_email_usuario(email: EmailUpdate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return UserService.update_email_usuario(db=db, email=email, user_id=user_id)