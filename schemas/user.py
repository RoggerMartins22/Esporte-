from pydantic import BaseModel, validator
import re
from fastapi import HTTPException, status

class UserBase(BaseModel):
    nome: str
    email: str

class UserCreate(UserBase):
    senha: str

class LoginRequest(BaseModel):
    email: str
    senha: str
    
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True