from uuid import UUID
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from apps.base.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.base.validator.user_validator import UserValidator
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.mapper.mapper_schema import map_schema_to_model_dict
from apps.base.entity.user import User
from apps.base.entity.client import Client


def create_user(user_data: UserCreateRequest) -> UserCreateResponse:
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

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.CLIENT_NOT_FOUND,
                status_code=400,
                message=f"Client com ID {client_id} não encontrado."
            )

    user_instance = map_schema_to_model_dict(user_data, User)
    user_instance.password = make_password(user_data.password)
    user_instance.client = None if user_data.is_superuser else client

    user_instance.save()
    return UserCreateResponse.model_validate(user_instance)


def get_user(user_id: UUID) -> UserResponse:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.USER_NOT_FOUND,
            status_code=404,
            message=f"Usuário com ID {user_id} não encontrado."
        )
    return UserResponse.model_validate(user)


def get_user_by_email(email: str) -> UserResponse:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.USER_NOT_FOUND,
            status_code=404,
            message=f"Usuário com email {email} não encontrado."
        )
    return UserResponse.model_validate(user)


def update_user(user_id: UUID, data: UserUpdateRequest) -> UserResponse:
    UserValidator.validate_user_update(data)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.USER_NOT_FOUND,
            status_code=404,
            message=f"Usuário com ID {user_id} não encontrado."
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    user.save()
    return UserResponse.model_validate(user)


def verify_user(user_id: UUID) -> UserResponse:
    """Marca o usuário como verificado."""
    return update_user(user_id, UserUpdateRequest(is_verified=True))
