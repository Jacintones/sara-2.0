from typing import List, Optional
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.entity.client import Client

class ClientRepository:
    """Repositório para operações com Clients."""

    def create_client(self, client: Client) -> Client:
        """Cria um novo client."""
        try:
            client.save()
            return client
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_CLIENT,
                status_code=400,
                message=f"Erro ao criar client",
                details=str(e)
            )


    def list_clients(self) -> List[Client]:
        """Lista todos os clients."""
        try:
            return list(Client.objects.all())
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_CLIENTS,
                status_code=400,
                message=f"Erro ao listar clients",
                details=str(e)
            )

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Obtém um client pelo id."""
        try:
            return Client.objects.get(id=client_id)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_CLIENT,
                status_code=400,
                message=f"Erro ao buscar client",
                details=str(e)
            )
