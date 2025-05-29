from django.contrib.auth.hashers import make_password
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse
from apps.users.models import User
from apps.users.repository.user_repository import UserRepository
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase
from apps.tenants.models import Tenant
from django.core.exceptions import ObjectDoesNotExist

class UserService:
    """Serviço para gerenciamento de usuários."""
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa o serviço com suas dependências.
        
        Args:
            user_repository: Repositório de usuários
        """
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreateRequest) -> UserCreateResponse:
        data = user_data.model_dump()
        data["password"] = make_password(user_data.password)
        
        tenant_id = data.get("tenant_id")

        if tenant_id is not None:
            if not Tenant.objects.filter(id=tenant_id).exists():
                raise ExceptionBase(
                    type_error=ErrorType.TENANT_NOT_FOUND,
                    status_code=400,
                    message=f"Tenant com ID {tenant_id} não encontrado."
                )

        user = self.user_repository.create_user_from_dict(data)
        return UserCreateResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserCreateResponse:
        user = User.objects.get(id=user_id)
        return UserCreateResponse.model_validate(user)
    
    def get_user_by_email(self, email: str) -> UserCreateResponse:
        user = self.user_repository.get_user_by_email(email)
        return UserCreateResponse.model_validate(user)
