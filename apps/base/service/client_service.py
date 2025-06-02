from typing import List, Optional
from django.db import transaction
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.mapper.mapper_schema import map_schema_to_model_dict
from apps.base.repository.client_repository import ClientRepository
from apps.base.dto.client_dto import ClientCreateRequest, ClientCreatedResponse, ClientListResponse
from apps.base.entity.client import Client
from apps.base.validator.client_validator import ClientValidator
from utils.validators import BusinessValidator

class ClientService:    
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, data: ClientCreateRequest) -> ClientCreatedResponse:
        """Cria um novo cliente."""
        ClientValidator.validate_client_data(data)

        client = map_schema_to_model_dict(data, Client)
        client = self.repository.create_client(client)
        return ClientCreatedResponse.model_validate(client)

    def list_clients(self) -> list[ClientListResponse]:
        """Lista todos os clientes."""
        clients = self.repository.list_clients()
        return [ClientListResponse.model_validate(client) for client in clients]



