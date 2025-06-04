from pydantic import BaseModel
import enum

class StatusEnum(str, enum.Enum):
    A = "A" 
    C = "C"

class PermissaoEnum(str, enum.Enum):
    USER = "USER"
    ADM = "ADM"

class UserBase(BaseModel):
    nome: str
    email: str
    cpf: str

class UserCreate(UserBase):
    senha: str

class LoginRequest(BaseModel):
    cpf: str
    senha: str

class UserInfoResponse(BaseModel):
    id: int
    cpf: str
    nome: str
    email: str
    
class ResetPasswordRequest(BaseModel):
    cpf: str
    email: str

class ValidatePasswordRequest(BaseModel):
    nova_senha: str

class NomeUpdate(BaseModel):
    nome: str 

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True