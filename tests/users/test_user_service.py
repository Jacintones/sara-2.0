import pytest
from unittest.mock import Mock, patch
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.users.service.user_service import UserService


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def user_service(repository_mock):
    return UserService(repository=repository_mock)


@pytest.fixture
def valid_user_data():
    return UserCreateRequest(
        first_name="Test",
        last_name="User",
        email="valid@example.com",
        password="ValidPassword123!",
        is_superuser=False,
        is_staff=False,
        tenant_id=1
    )


def test_create_user_success(user_service, repository_mock, valid_user_data):
    with patch("utils.validators.BusinessValidator.validate_email", return_value=True), \
         patch("utils.validators.BusinessValidator.validate_password", return_value=(True, None)), \
         patch("apps.tenants.models.Tenant.objects.filter") as tenant_filter:

        tenant_filter.return_value.exists.return_value = True
        user_dict = valid_user_data.model_dump()
        user_dict.update({
            "id": 1,
            "is_verified": False,
            "is_active": True
        })
        repository_mock.create_user_from_dict.return_value = user_dict

        result = user_service.create_user(valid_user_data)

        assert isinstance(result, UserCreateResponse)
        assert result.email == valid_user_data.email


def test_create_user_invalid_email(user_service, valid_user_data):
    with patch("utils.validators.BusinessValidator.validate_email", return_value=False):
        with pytest.raises(ExceptionBase) as exc:
            user_service.create_user(valid_user_data)

        assert exc.value.type_error == ErrorType.INVALID_EMAIL


def test_create_user_invalid_password(user_service, valid_user_data):
    with patch("utils.validators.BusinessValidator.validate_email", return_value=True), \
         patch("utils.validators.BusinessValidator.validate_password", return_value=(False, "Senha inválida")):
        
        with pytest.raises(ExceptionBase) as exc:
            user_service.create_user(valid_user_data)

        assert exc.value.type_error == ErrorType.INVALID_PASSWORD


def test_create_user_without_tenant(user_service, valid_user_data):
    valid_user_data.tenant_id = None

    with patch("utils.validators.BusinessValidator.validate_email", return_value=True), \
         patch("utils.validators.BusinessValidator.validate_password", return_value=(True, None)):

        with pytest.raises(ExceptionBase) as exc:
            user_service.create_user(valid_user_data)

        assert exc.value.type_error == ErrorType.TENANT_REQUIRED


def test_create_user_tenant_not_found(user_service, valid_user_data):
    with patch("utils.validators.BusinessValidator.validate_email", return_value=True), \
         patch("utils.validators.BusinessValidator.validate_password", return_value=(True, None)), \
         patch("apps.tenants.models.Tenant.objects.filter") as tenant_filter:

        tenant_filter.return_value.exists.return_value = False

        with pytest.raises(ExceptionBase) as exc:
            user_service.create_user(valid_user_data)

        assert exc.value.type_error == ErrorType.TENANT_NOT_FOUND


def test_get_user_success(user_service, repository_mock):
    user_dict = {
        "id": 1,
        "email": "test@test.com",
        "first_name": "T",
        "last_name": "U",
        "tenant_id": 1,
        "is_verified": True,
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    repository_mock.get_user_by_id.return_value = user_dict

    result = user_service.get_user(1)
    assert isinstance(result, UserResponse)
    assert result.id == 1


def test_get_user_not_found(user_service, repository_mock):
    repository_mock.get_user_by_id.return_value = None

    with pytest.raises(ExceptionBase) as exc:
        user_service.get_user(99)

    assert exc.value.type_error == ErrorType.USER_NOT_FOUND  


def test_get_user_by_email_success(user_service, repository_mock):
    user_dict = {
        "id": 2,
        "email": "email@test.com",
        "first_name": "E",
        "last_name": "U",
        "tenant_id": 1,
        "is_verified": True,
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    repository_mock.get_user_by_email.return_value = user_dict

    result = user_service.get_user_by_email("email@test.com")
    assert isinstance(result, UserResponse)
    assert result.email == "email@test.com"


def test_get_user_by_email_not_found(user_service, repository_mock):
    repository_mock.get_user_by_email.return_value = None

    with pytest.raises(ExceptionBase) as exc:
        user_service.get_user_by_email("notfound@test.com")

    assert exc.value.type_error == ErrorType.USER_NOT_FOUND


def test_update_user_success(user_service, repository_mock):
    update_data = UserUpdateRequest(
        email="new@test.com",
        first_name="New",
        last_name="Name",
        tenant_id=None,
        is_verified=True,
        is_active=True,
        is_staff=True,
        is_superuser=True
    )

    repository_mock.get_user_by_id.return_value = {
        "id": 1,
        "email": "old@test.com",
        "first_name": "Old",
        "last_name": "Name",
        "tenant_id": None,
        "is_verified": False,
        "is_active": True,
        "is_staff": True,
        "is_superuser": True
    }

    updated_user = {
        "id": 1,
        "email": update_data.email,
        "first_name": update_data.first_name,
        "last_name": update_data.last_name,
        "tenant_id": update_data.tenant_id,
        "is_verified": update_data.is_verified,
        "is_active": update_data.is_active,
        "is_staff": update_data.is_staff,
        "is_superuser": update_data.is_superuser
    }

    repository_mock.update_user.return_value = updated_user

    result = user_service.update_user(1, update_data)

    assert isinstance(result, UserResponse)
    assert result.email == "new@test.com"



def test_verify_user(user_service, repository_mock):
    user_dict = {
        "id": 10,
        "email": "v@me.com",
        "first_name": "V",
        "last_name": "M",
        "tenant_id": 1,
        "is_verified": False,
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }

    repository_mock.get_user_by_id.return_value = user_dict

    result = user_service.verify_user(10)

    assert isinstance(result, UserResponse)
    assert result.is_verified is True
    repository_mock.update_user.assert_called_with(10, {"is_verified": True})
