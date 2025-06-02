from datetime import timedelta
import logging
from django.contrib.auth.hashers import check_password
from apps.users.models import User
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.users.repository.user_repository import UserRepository
from django.db import connection
from django_tenants.utils import get_public_schema_name

from apps.accounts.dto.auth_dto import LoginRequest
from apps.accounts.dto.auth_dto import LoginResponse
from apps.accounts.auth.jwt_handler import create_access_token

logger = logging.getLogger(__name__)

class AuthService:
    """Serviço para autenticação de usuários."""
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, data: LoginRequest) -> LoginResponse:
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

            if user.is_superuser:
                current_schema = connection.schema_name
            else:
                if not user.tenant:
                    logger.error(f"[AuthService] Usuário {user.email} não possui tenant associado")
                    raise ExceptionBase(
                        type_error=ErrorType.INVALID_TENANT,
                        status_code=403,
                        message="Usuário não possui tenant associado."
                    )
                current_schema = user.tenant.schema_name

            expiration = timedelta(days=30 if data.remember_me else 1)
            payload = {
                "sub": str(user.id),
                "email": user.email,
                "tenant": current_schema,
                "roles": {
                    "is_superuser": user.is_superuser,
                    "is_staff": user.is_staff
                }
            }
            token = create_access_token(payload, expiration)
            logger.info(
                f"[AuthService] Login realizado com sucesso. "
                f"Usuário: {user.email}, "
                f"Tenant: {user.tenant.name if user.tenant else 'N/A'}, "
                f"Schema: {current_schema}, "
                f"Roles: superuser={user.is_superuser}, staff={user.is_staff}"
            )
            redirect_url = None
            if user.tenant:
                domain_obj = user.tenant.domains.first()
                if domain_obj:
                    redirect_url = f"https://{domain_obj.domain}"

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
                is_superuser=user.is_superuser,
                redirect_url=redirect_url 
            )
        except Exception as e:
            logger.exception(f"[AuthService] Erro inesperado durante o login: {str(e)}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LOGIN,
                status_code=500,
                message="Erro ao fazer login",
                details=str(e)
            )
