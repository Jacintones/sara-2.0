from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.users.models import User
from apps.users.repository.user_repository import UserRepository
from apps.tenants.models import Tenant
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase

class UserService:
    """Serviço para gerenciamento de usuários."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreateRequest) -> UserCreateResponse:
        """Cria um novo usuário a partir dos dados fornecidos."""
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

        user = self.repository.create_user_from_dict(data)
        return UserCreateResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        """Obtém um usuário pelo ID."""
        try:
            user = self.repository.get_user_by_id(user_id)
            return UserResponse.model_validate(user)
        except ObjectDoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=404,
                message=f"Usuário com ID {user_id} não encontrado."
            )
    
    def get_user_by_email(self, email: str) -> UserResponse:
        """Obtém um usuário pelo email."""
        try:
            user = self.repository.get_user_by_email(email)
            return UserResponse.model_validate(user)
        except ObjectDoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=404,
                message=f"Usuário com email {email} não encontrado."
            )
    
    def update_user(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        """Atualiza um usuário com os dados fornecidos."""
        updated_user = self.user_repository.update_user(user_id, data.model_dump(exclude_unset=True))
        return UserResponse.model_validate(updated_user)


    def verify_user(self, user_id: int) -> UserResponse:
        user = self.get_user(user_id)
        self.repository.update_user(user_id, {"is_verified": True})
        user.is_verified = True  
        return UserResponse.model_validate(user)

