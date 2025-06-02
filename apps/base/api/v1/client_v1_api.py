from ninja import Router
from apps.base.di import container
from apps.accounts.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum
from apps.base.core.exception.exception_base import ErrorResponse
from apps.base.dto.client_dto import ClientCreateRequest, ClientCreatedResponse, ClientListResponse

client_v1_router = Router(tags=["Clients"])

@client_v1_router.post("/", response={201: ClientCreatedResponse, 400: ErrorResponse, 403: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_client(request, data: ClientCreateRequest) -> ClientCreatedResponse:
    return 201, container.client_service().create_client(data)

@client_v1_router.get("/", response=list[ClientListResponse])
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN]) 
def list_clients(request):
    return container.client_service().list_clients()

@client_v1_router.get("/{client_id}", response=ClientListResponse)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def get_client(request, client_id: int):
    return container.client_service().get_client(client_id)
