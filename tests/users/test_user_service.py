import pytest
from unittest.mock import MagicMock, patch

from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

from apps.users.service.user_service import UserService
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest

# Supondo que existe uma função que mapeia o schema para dict/model
from config.core.mapper.mapper_schema import map_schema_to_model_dict

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_tenant_repository():
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repository, mock_tenant_repository):
    return UserService(mock_user_repository, mock_tenant_repository)

def test_create_user_superuser(user_service, mock_user_repository, mock_tenant_repository, monkeypatch):
    data = UserCreateRequest(
        email="admin@email.com", first_name="Admin", last_name="Root",
        password="Senha123!", tenant_id=1, is_superuser=True, is_staff=True
    )
    mock_user = MagicMock()
    mock_user_repository.create_user.return_value = mock_user

    monkeypatch.setattr("apps.users.validators.user_validator.UserValidator.validate_user_creation", lambda x: None)
    monkeypatch.setattr("config.core.mapper.mapper_schema.map_schema_to_model_dict", lambda data, model: mock_user)
    monkeypatch.setattr("django.contrib.auth.hashers.make_password", lambda pwd: "hashed_"+pwd)
    monkeypatch.setattr("apps.users.dto.user_dto.UserCreateResponse.model_validate", lambda user: "usercreate_response")

    result = user_service.create_user(data)
    assert result == "usercreate_response"
    mock_user_repository.create_user.assert_called_once()

def test_create_user_missing_tenant(user_service, monkeypatch):
    data = UserCreateRequest(
        email="user@email.com", first_name="U", last_name="S",
        password="Senha123!", tenant_id=None, is_superuser=False, is_staff=False
    )
    monkeypatch.setattr("apps.users.validators.user_validator.UserValidator.validate_user_creation", lambda x: None)

    with pytest.raises(ExceptionBase) as excinfo:
        user_service.create_user(data)
    assert excinfo.value.type_error == ErrorType.TENANT_REQUIRED

def test_create_user_tenant_not_found(user_service, mock_tenant_repository, monkeypatch):
    data = UserCreateRequest(
        email="user@email.com", first_name="U", last_name="S",
        password="Senha123!", tenant_id=2, is_superuser=False, is_staff=False
    )
    mock_tenant_repository.get_tenant_by_id.return_value = None
    monkeypatch.setattr("apps.users.validators.user_validator.UserValidator.validate_user_creation", lambda x: None)

    with pytest.raises(ExceptionBase) as excinfo:
        user_service.create_user(data)
    assert excinfo.value.type_error == ErrorType.TENANT_NOT_FOUND

def test_get_user_success(user_service, mock_user_repository, monkeypatch):
    user_id = 1
    mock_user = MagicMock()
    mock_user_repository.get_user_by_id.return_value = mock_user
    monkeypatch.setattr("apps.users.dto.user_dto.UserResponse.model_validate", lambda user: "user_response")
    result = user_service.get_user(user_id)
    assert result == "user_response"
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)

def test_get_user_not_found(user_service, mock_user_repository):
    user_id = 2
    mock_user_repository.get_user_by_id.return_value = None
    with pytest.raises(ExceptionBase) as excinfo:
        user_service.get_user(user_id)
    assert excinfo.value.type_error == ErrorType.USER_NOT_FOUND

def test_get_user_by_email_success(user_service, mock_user_repository, monkeypatch):
    email = "test@email.com"
    mock_user = MagicMock()
    mock_user_repository.get_user_by_email.return_value = mock_user
    monkeypatch.setattr("apps.users.dto.user_dto.UserResponse.model_validate", lambda user: "user_response")
    result = user_service.get_user_by_email(email)
    assert result == "user_response"
    mock_user_repository.get_user_by_email.assert_called_once_with(email)

def test_get_user_by_email_not_found(user_service, mock_user_repository):
    email = "test@email.com"
    mock_user_repository.get_user_by_email.return_value = None
    with pytest.raises(ExceptionBase) as excinfo:
        user_service.get_user_by_email(email)
    assert excinfo.value.type_error == ErrorType.USER_NOT_FOUND

def test_update_user_success(user_service, mock_user_repository, monkeypatch):
    user_id = 1
    data = UserUpdateRequest(username="user", email="user@email.com", first_name="U", last_name="S")
    mock_user = MagicMock()
    mock_user_repository.get_user_by_id.return_value = mock_user
    mock_user_repository.update_user.return_value = mock_user
    monkeypatch.setattr("apps.users.validators.user_validator.UserValidator.validate_user_update", lambda x: None)
    monkeypatch.setattr("apps.users.dto.user_dto.UserResponse.model_validate", lambda user: "user_response")
    result = user_service.update_user(user_id, data)
    assert result == "user_response"
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user.assert_called_once()

def test_verify_user_success(user_service, mock_user_repository, monkeypatch):
    user_id = 1
    data = UserUpdateRequest(is_verified=True)
    mock_user = MagicMock()
    mock_user_repository.get_user_by_id.return_value = mock_user
    mock_user_repository.update_user.return_value = mock_user
    monkeypatch.setattr("apps.users.validators.user_validator.UserValidator.validate_user_update", lambda x: None)
    monkeypatch.setattr("apps.users.dto.user_dto.UserResponse.model_validate", lambda user: "user_response")
    result = user_service.verify_user(user_id)
    assert result == "user_response"

