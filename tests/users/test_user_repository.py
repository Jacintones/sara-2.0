import pytest
from unittest.mock import patch, MagicMock
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from apps.users.repository.user_repository import UserRepository
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType


@pytest.fixture
def repo():
    return UserRepository()


def test_create_user_success(repo):
    with patch("apps.users.models.User.objects.create") as mock_create:
        mock_create.return_value = MagicMock()
        result = repo.create_user_from_dict({"email": "test@example.com"})
        assert result is not None
        assert mock_create.called


def test_create_user_integrity_error(repo):
    with patch("apps.users.models.User.objects.create", side_effect=IntegrityError("Violação de integridade")):
        with pytest.raises(ExceptionBase) as exc:
            repo.create_user_from_dict({"email": "duplicado@example.com"})
        assert exc.value.type_error == ErrorType.ERROR_CREATE_USER


def test_get_user_by_id_success(repo):
    mock_user = MagicMock()
    with patch("apps.users.models.User.objects.get", return_value=mock_user):
        result = repo.get_user_by_id(1)
        assert result == mock_user


def test_get_user_by_id_not_found(repo):
    with patch("apps.users.models.User.objects.get", side_effect=ObjectDoesNotExist):
        with pytest.raises(ExceptionBase) as exc:
            repo.get_user_by_id(999)
        assert exc.value.type_error == ErrorType.USER_NOT_FOUND


def test_get_user_by_id_unexpected_error(repo):
    with patch("apps.users.models.User.objects.get", side_effect=Exception("Erro")):
        with pytest.raises(ExceptionBase) as exc:
            repo.get_user_by_id(1)
        assert exc.value.type_error == ErrorType.ERROR_GET_USER


def test_get_user_by_email_success(repo):
    mock_user = MagicMock()
    with patch("apps.users.models.User.objects.get", return_value=mock_user):
        result = repo.get_user_by_email("test@example.com")
        assert result == mock_user


def test_get_user_by_email_not_found(repo):
    with patch("apps.users.models.User.objects.get", side_effect=ObjectDoesNotExist):
        with pytest.raises(ExceptionBase) as exc:
            repo.get_user_by_email("naoexiste@example.com")
        assert exc.value.type_error == ErrorType.EMAIL_NOT_FOUND


def test_get_user_by_email_unexpected_error(repo):
    with patch("apps.users.models.User.objects.get", side_effect=Exception("Erro")):
        with pytest.raises(ExceptionBase) as exc:
            repo.get_user_by_email("erro@example.com")
        assert exc.value.type_error == ErrorType.ERROR_GET_USER


def test_update_user_success(repo):
    mock_user = MagicMock()
    with patch.object(UserRepository, "get_user_by_id", return_value=mock_user):
        mock_user.save = MagicMock()
        result = repo.update_user(1, {"first_name": "Novo"})
        assert result == mock_user
        assert mock_user.first_name == "Novo"
        assert mock_user.save.called


def test_update_user_fails(repo):
    with patch.object(UserRepository, "get_user_by_id", side_effect=Exception("Falha")):
        with pytest.raises(ExceptionBase) as exc:
            repo.update_user(1, {"first_name": "Erro"})
        assert exc.value.type_error == ErrorType.ERROR_UPDATE_USER
