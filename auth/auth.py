from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from schemas.user import UserBase
from fastapi import HTTPException, status
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def token_verifier(token = Depends(oauth_scheme)):
    OAuth2.verify_token(access_token=token)

class OAuth2:
    @staticmethod
    def user_login(user: UserBase, expires_in: int = 30):

            exp = datetime.utcnow() + timedelta(minutes=expires_in)
            
            payload = {
                'sub': user.email,
                'exp': exp
            }

            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            return {
                'access_token': access_token,
                'exp': exp,
                'detail': "Login realizado com sucesso!"
            }
        
    @staticmethod
    def verify_token(access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Acesso Inválido!!"
        )