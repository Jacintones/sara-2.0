import logging
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from django.core.exceptions import ObjectDoesNotExist

from apps.base.entity.user import User

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository para operações com usuários."""
    def create_user(self, user: User) -> User:
        try:
            user.save()
            return user
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao criar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_USER,
                status_code=500,
                message=f"Erro inesperado ao criar usuário",
                details=str(e)
            )

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao buscar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_USER,
                status_code=500,
                message=f"Erro inesperado ao buscar usuário: {e}",
                details=str(e)
            )

    def get_user_by_email(self, email: str) -> User:
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.EMAIL_NOT_FOUND,
                status_code=404,
                message=f"E-mail não encontrado",
                details=str(e)  
            )
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao buscar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_USER,
                status_code=500,
                message=f"Erro inesperado ao buscar usuário: {e}",
                details=str(e)
            )

    def update_user(self, user : User) -> User:
        try:
            user.save()
            return user
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao atualizar usuário",
                status_code=400,
                type_error=ErrorType.ERROR_UPDATE_USER,
                details=str(e)
            )

    

