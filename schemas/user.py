from pydantic import BaseModel

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