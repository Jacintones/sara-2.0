from typing import Tuple
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from utils.validators import BusinessValidator
from apps.base.dto.user_dto import UserCreateRequest, UserUpdateRequest


class UserValidator:
    """Validador específico para regras de negócio relacionadas a usuários."""

    @staticmethod
    def validate_user_creation(user_data: UserCreateRequest) -> None:
        """
        Valida os dados para criação de um usuário.
        """
        UserValidator._validate_email(user_data.email)
        UserValidator._validate_password(user_data.password)

    @staticmethod
    def validate_user_update(user_data: UserUpdateRequest) -> None:
        """
        Valida os dados para atualização de um usuário.
        Só valida os campos que estiverem presentes (parciais).
        """
        if user_data.email is not None:
            UserValidator._validate_email(user_data.email)


    @staticmethod
    def _validate_email(email: str) -> None:
        if not BusinessValidator.validate_email(email):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_EMAIL,
                status_code=400,
                message="O email é inválido."
            )

    @staticmethod
    def _validate_password(password: str) -> None:
        senha_valida, erro = BusinessValidator.validate_password(password)
        if not senha_valida:
            raise ExceptionBase(
                type_error=ErrorType.INVALID_PASSWORD,
                status_code=400,
                message=erro or "A senha é inválida."
            )

