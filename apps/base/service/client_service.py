from typing import List, Optional
from django.db import transaction
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.mapper.mapper_schema import map_schema_to_model_dict
from apps.base.dto.client_dto import ClientCreateRequest, ClientCreatedResponse, ClientListResponse
from apps.base.entity.client import Client
from apps.base.validator.client_validator import ClientValidator
from utils.validators import BusinessValidator


def create_client(data: ClientCreateRequest) -> ClientCreatedResponse:
    """Cria um novo cliente."""
    try:
        ClientValidator.validate_client_data(data)
    
        client = map_schema_to_model_dict(data, Client)
        client.save()
        return ClientCreatedResponse.model_validate(client)
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.ERROR_CREATE_CLIENT,
            message="Ocorreu um erro ao criar cliente.",
            status_code=400,
            details=str(e)
        )

def list_clients() -> list[ClientListResponse]:
    """Lista todos os clientes."""
    try:
        clients = Client.objects.all()
        return [ClientListResponse.model_validate(client) for client in clients]
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.ERROR_LIST_CLIENTS,
            message="Ocorreu um erro ao listar clientes.",
            status_code=400,
            details=str(e)
        )
