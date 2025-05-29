from datetime import timedelta
import logging
from django.contrib.auth.hashers import check_password
from apps.users.models import User
from config.core.auth.jwt_handler import create_access_token
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.users.dto.auth_dto import LoginRequest, LoginResponse
from apps.users.repository.user_repository import UserRepository
from django.db import connection

logger = logging.getLogger(__name__)

class AuthService:
    """Serviço para autenticação de usuários."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, data: LoginRequest) -> LoginResponse:
        """
        Realiza o login do usuário.
        
        Se o usuário tiver um tenant associado, valida se ele está acessando
        pelo schema correto. Caso contrário, permite o acesso em qualquer schema.
        """
        logger.info(f"[AuthService] Tentativa de login para o email: {data.email}")
        
        try:
            user = self.repository.get_user_by_email(data.email)

            if not user:
                logger.warning(f"[AuthService] Email não encontrado: {data.email}")
                raise ExceptionBase(
                    type_error=ErrorType.EMAIL_NOT_FOUND,
                    status_code=401,
                    message="E-mail não encontrado."
                )

            if not check_password(data.password, user.password):
                logger.warning(f"[AuthService] Senha inválida para o usuário: {user.email}")
                raise ExceptionBase(
                    type_error=ErrorType.INVALID_CREDENTIALS,
                    status_code=401,
                    message="Senha inválida."
                )

            if not user.is_active:
                logger.warning(f"[AuthService] Tentativa de login de usuário inativo: {user.email}")
                raise ExceptionBase(
                    type_error=ErrorType.INACTIVE_USER,
                    status_code=403,
                    message="Usuário inativo."
                )

            schema_atual = connection.schema_name
            
            if user.tenant:
                if user.tenant.schema_name != schema_atual:
                    logger.warning(
                        f"[AuthService] Tentativa de acesso com tenant inválido. "
                        f"Usuario: {user.email}, Schema esperado: {user.tenant.schema_name}, "
                        f"Schema atual: {schema_atual}"
                    )
                    raise ExceptionBase(
                        type_error=ErrorType.INVALID_TENANT,
                        status_code=403,
                        message="Usuário não pertence a este tenant."
                    )
            else:
                logger.info(f"[AuthService] Usuário {user.email} não possui tenant associado")

            expiration = timedelta(days=30 if data.remember_me else 1)
            payload = {
                "sub": str(user.id), 
                "email": user.email, 
                "tenant": schema_atual if user.tenant else None
            }
            
            token = create_access_token(payload, expiration)

            logger.info(
                f"[AuthService] Login realizado com sucesso. "
                f"Usuário: {user.email}, Tenant: {schema_atual if user.tenant else 'N/A'}, "
                f"Remember Me: {data.remember_me}"
            )
            
            return LoginResponse(
                access_token=token,
                user_id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_verified=user.is_verified,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser
            )
            
        except Exception as e:
            logger.exception(f"[AuthService] Erro inesperado durante o login: {str(e)}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LOGIN,
                status_code=500,
                message=str(e)
            )
