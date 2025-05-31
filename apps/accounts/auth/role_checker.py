from functools import wraps
from typing import List, Union
from apps.users.enums.role_enum import RoleEnum
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

logger = __import__('logging').getLogger(__name__)

def check_role(required_roles: Union[RoleEnum, List[RoleEnum]]):
    """
    Decorator para verificar se o usuário tem os roles necessários.
    
    Args:
        required_roles: Role ou lista de roles necessários para acessar a rota
        
    Exemplo de uso:
        @router.get("/admin-only")
        @check_role(RoleEnum.ADMIN)
        def admin_only(request):
            return {"message": "Você é admin!"}
            
        @router.get("/admin-or-user")
        @check_role([RoleEnum.ADMIN, RoleEnum.USER])
        def admin_or_user(request):
            return {"message": "Você tem acesso!"}
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            roles = [required_roles] if isinstance(required_roles, RoleEnum) else required_roles
            logger.info(f"Verificando roles: {roles} para o usuário: {getattr(request, 'auth', None)}")
            if not hasattr(request, 'auth') or not request.auth:
                raise ExceptionBase(
                    type_error=ErrorType.UNAUTHORIZED_ERROR,
                    status_code=401,
                    message="Não autenticado"
                )
        
            user_roles = request.auth.get('roles', {})
            if not user_roles:
                raise ExceptionBase(
                    type_error=ErrorType.UNAUTHORIZED_ERROR,
                    status_code=401,
                    message="Informações de roles não encontradas"
                )
            
            user = type('User', (), {
                'is_superuser': user_roles.get('is_superuser', False),
                'is_staff': user_roles.get('is_staff', False)
            })
            
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