from functools import wraps
from typing import List, Union
from apps.base.enum.role_enum import RoleEnum
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType

logger = __import__('logging').getLogger(__name__)

def check_role(required_roles: Union[RoleEnum, List[RoleEnum]]):
    """
    Decorador para verificar se o usuário tem os roles necessários.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            roles = [required_roles] if isinstance(required_roles, RoleEnum) else required_roles

            user = getattr(request, "user", None)
            logger.info(f"Usuário autenticado: {user}")
            logger.info(f"token do usuário: {getattr(request, 'auth', None)}")
            if user is None or not user.is_authenticated:
                raise ExceptionBase(
                    type_error=ErrorType.UNAUTHORIZED_ERROR,
                    status_code=401,
                    message="Usuário não autenticado"
                )

            logger.info(f"Verificando roles {roles} para o usuário: {user.email}")

            for role in roles:
                if RoleEnum.has_role(user, role): 
                    return func(request, *args, **kwargs)

            raise ExceptionBase(
                type_error=ErrorType.UNAUTHORIZED_ERROR,
                status_code=403,
                message="Sem permissão para acessar este recurso",
                details=f"Usuário não possui os roles necessários: {roles}"
            )

        return wrapper
    return decorator
