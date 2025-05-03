from datetime import datetime, timedelta
from passlib.context import CryptContext
from schemas.user import UserBase
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthHandler:
    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    
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