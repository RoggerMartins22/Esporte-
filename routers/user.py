from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.user import (create_user_service, login_user_service)
from auth.auth import token_verifier
from schemas.user import UserCreate, LoginRequest
from database import get_db

router = APIRouter(
    prefix="/usuario",
    tags=["users"],
)
test = APIRouter(
    prefix="/test",
    tags=["test"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/cadastrar")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db=db, user=user)

@router.post("/login")
async def login_user(request_form_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = LoginRequest(
        email=request_form_user.username,
        senha=request_form_user.password
    )

    return login_user_service(db=db, user=user)

@test.get('/')
def test_user_verify():
    return 'Está ok'