from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.users.models import User
from apps.users.repository.user_repository import UserRepository
from apps.users.validators.user_validator import UserValidator
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase
from apps.tenants.repository.tenant_repository import TenantRepository
from config.core.mapper.mapper_schema import map_schema_to_model_dict


class UserService:
    """Serviço para gerenciamento de usuários."""

    def __init__(self, repository: UserRepository, tenant_repository: TenantRepository):
        self.repository = repository
        self.tenant_repository = tenant_repository

    def create_user(self, user_data: UserCreateRequest) -> UserCreateResponse:
        UserValidator.validate_user_creation(user_data)
        tenant = None
        tenant_id = user_data.tenant_id

        if not user_data.is_superuser:
            if tenant_id is None:
                raise ExceptionBase(
                    type_error=ErrorType.TENANT_REQUIRED,
                    status_code=400,
                    message="A tenant é obrigatória para usuários não superusuários."
                )
            tenant = self.tenant_repository.get_tenant_by_id(tenant_id)
            if not tenant:
                raise ExceptionBase(
                    type_error=ErrorType.TENANT_NOT_FOUND,
                    status_code=400,
                    message=f"Tenant com ID {tenant_id} não encontrado."
                )

        data = user_data.model_dump()
        if data.get("is_superuser"):
            data["tenant_id"] = None

        user_instance = map_schema_to_model_dict(user_data, User)
        if not user_data.is_superuser:
            user_instance.tenant = tenant  
        else:
            user_instance.tenant = None   

        user_instance.password = make_password(user_data.password)

        user = self.repository.create_user(user_instance)
        return UserCreateResponse.model_validate(user)


    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=404,
                message=f"Usuário com ID {user_id} não encontrado."
            )
        return UserResponse.model_validate(user)

    def get_user_by_email(self, email: str) -> UserResponse:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=404,
                message=f"Usuário com email {email} não encontrado."
            )
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        UserValidator.validate_user_update(data)
        user = self.repository.get_user_by_id(user_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
            
        user_updated = self.repository.update_user(user)
        return UserResponse.model_validate(user_updated)


    def verify_user(self, user_id: int) -> UserResponse:
        request = UserUpdateRequest(is_verified=True)
        user = self.update_user(user_id, request)
        return UserResponse.model_validate(user)

