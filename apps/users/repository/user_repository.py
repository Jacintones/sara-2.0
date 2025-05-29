import logging
from typing import Optional
from django.db import IntegrityError
from apps.users.models import User
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository para operações com usuários."""
    
    def create_user_from_dict(self, data: dict) -> User:
        try:
            user = User.objects.create(**data)
            return user
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao criar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_USER,
                status_code=500,
                message=f"Erro inesperado ao criar usuário: {e}"
            )

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=404,
                message=f"Usuário não encontrado"
            )
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao buscar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_USER,
                status_code=500,
                message=f"Erro inesperado ao buscar usuário: {e}"
            )
        
    def get_user_by_email(self, email: str) -> User:
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.EMAIL_NOT_FOUND,
                status_code=404,
                message=f"E-mail não encontrado"
            )
        except Exception as e:
            logger.exception(f"[Exception] Erro inesperado ao buscar usuário: {e}")
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_USER,
                status_code=500,
                message=f"Erro inesperado ao buscar usuário: {e}"
            )

