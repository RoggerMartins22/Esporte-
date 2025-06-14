from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from repository.usuarios import UserRepository
from auth.hashing import AuthHandler
from auth.auth import OAuth2
from auth.token_handler import generate_expiration, generate_token
from schemas.usuarios import UserCreate, LoginRequest, UserInfoResponse, ResetPasswordRequest, ValidatePasswordRequest, NomeUpdate, EmailUpdate
from mails.sendMail import send_email, send_email_reset_password
from datetime import datetime, timezone
import re

class UserService:

    @staticmethod
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
        
    @staticmethod
    def create_user_service(db: Session, user: UserCreate):

        UserService.validate_user_info(user)

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
                send_email(user)
                
                return {
                    "status_code": status.HTTP_201_CREATED,
                    "detail": "Usuário cadastrado com sucesso!"
                }

        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e) 
            )

    @staticmethod            
    def login_user_service(db: Session, user: LoginRequest):
        user_db = UserRepository.get_user_by_cpf(db=db, cpf=user.cpf)

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado"
            )
        
        elif user_db.status == "C":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Conta inativa. Entre em contato com o suporte."
            )
        
        elif not AuthHandler.verify_password(user.senha, user_db.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CPF ou senha incorreta!"
            )
        
        return OAuth2.user_login(user_db)

    @staticmethod
    def enviar_email_redefinicao_senha(db: Session, user: ResetPasswordRequest):

        user_db = UserRepository.get_user_by_email_cpf(db=db, user=user)
                                                
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado ou conta inativa."
            )
        
        token = generate_token()
        expiration = generate_expiration()

        UserRepository.save_token(db, token=token, email=user.email, expiration=expiration)

        send_email_reset_password(email=user.email, nome=user_db.nome, token=token)
        
        return {"detail": "Se os dados informados estiverem corretos, um e-mail será enviado."}

    @staticmethod
    def redefinir_senha_com_token(db, token, nova_senha: ValidatePasswordRequest):
        
        token_record = UserRepository.get_token_record(db, token)

        if not token_record or token_record.expiration < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Token inválido ou expirado.")

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", nova_senha.nova_senha):
            raise HTTPException(status_code=400, detail="Senha insegura.")

        user_db = UserRepository.get_user_by_email(db, email=token_record.email)

        if not user_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        user_db.senha = AuthHandler.hash_password(nova_senha.nova_senha)

        try:
            UserRepository.update_user_password(db=db, user_db=user_db)
            UserRepository.invalidate_token(db, token_record)
            
            return {"detail": "Senha redefinida com sucesso!"}
            
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
    @staticmethod
    def consulta_info_usuarios(db: Session, user_id: int):
        user = UserRepository.get_info_user(db=db, id_usuario=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        return UserInfoResponse(
            id=user.id,
            cpf=user.cpf,
            nome=user.nome,
            email=user.email
        )

    def update_nome_usuario(db: Session, nome: NomeUpdate, user_id: int):
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome.nome):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome inválido. Deve conter apenas letras."
            )

        user = UserRepository.get_info_user(db=db, id_usuario=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        user.nome = nome.nome
        
        try:
            UserRepository.update_user_date(db=db, user=user)
            return {"detail": "Nome atualizado com sucesso!"}
            
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    @staticmethod
    def update_email_usuario(db: Session, email: EmailUpdate, user_id: int):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail inválido."
            )

        user = UserRepository.get_info_user(db=db, id_usuario=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        if UserRepository.get_user_by_email(db=db, email=email.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um usuário com este e-mail cadastrado."
            )
        
        user.email = email.email
        
        try:
            UserRepository.update_user_date(db=db, user=user)
            return {"detail": "E-mail atualizado com sucesso!"}
            
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )