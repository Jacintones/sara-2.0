from django.contrib.auth.hashers import check_password
from apps.users.models import User
from config.core.auth.jwt_handler import create_access_token
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.users.dto.login_dto import LoginRequest, LoginResponse
from apps.users.repository.user_repository import UserRepository
from django.db import connection

class AuthService:
    """Serviço para autenticação de usuários."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, data: LoginRequest) -> LoginResponse:
        user = self.user_repository.get_user_by_email(data.email)

        if not user:
            raise ExceptionBase(
                type_error=ErrorType.EMAIL_NOT_FOUND,
                status_code=401,
                message="E-mail não encontrado."
            )

        if not check_password(data.password, user.password):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CREDENTIALS,
                status_code=401,
                message="Senha inválida."
            )

        if not user.is_active:
            raise ExceptionBase(
                type_error=ErrorType.INACTIVE_USER,
                status_code=403,
                message="Usuário inativo."
            )

        # Verifica se o schema atual é compatível com o tenant do usuário
        schema_atual = connection.schema_name
        if user.tenant.schema_name != schema_atual:
            raise ExceptionBase(
                type_error=ErrorType.INVALID_TENANT,
                status_code=403,
                message="Usuário não pertence a este tenant."
            )

        payload = {"sub": str(user.id), "email": user.email, "tenant": schema_atual}
        token = create_access_token(payload)

        return LoginResponse(access_token=token)
