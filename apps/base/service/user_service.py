from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from apps.base.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.base.validator.user_validator import UserValidator
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.mapper.mapper_schema import map_schema_to_model_dict
from apps.base.repository.user_repository import UserRepository
from apps.base.entity.user import User


class UserService:
    """Serviço para gerenciamento de usuários."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreateRequest) -> UserCreateResponse:
        UserValidator.validate_user_creation(user_data)
        client = None
        client_id = user_data.client_id

        if not user_data.is_superuser:
            if client_id is None:
                raise ExceptionBase(
                    type_error=ErrorType.CLIENT_REQUIRED,
                    status_code=400,
                    message="O client é obrigatório para usuários não superusuários."
                )
            client = self.client_repository.get_client_by_id(client_id)
            if not client:
                raise ExceptionBase(
                    type_error=ErrorType.CLIENT_NOT_FOUND,
                    status_code=400,
                    message=f"Client com ID {client_id} não encontrado."
                )

        data = user_data.model_dump()
        if data.get("is_superuser"):
            data["client_id"] = None

        user_instance = map_schema_to_model_dict(user_data, User)
        if not user_data.is_superuser:
            user_instance.client = client
        else:
            user_instance.client = None

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

