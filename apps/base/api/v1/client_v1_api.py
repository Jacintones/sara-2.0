from ninja import Router
from apps.authenticate.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum
from apps.base.core.exception.exception_base import ErrorResponse
from apps.base.dto.client_dto import ClientCreateRequest, ClientCreatedResponse, ClientListResponse
from apps.base.service.client_service import create_client, list_clients

client_v1_router = Router(tags=["Clients"])

@client_v1_router.post("/", response={201: ClientCreatedResponse, 400: ErrorResponse, 403: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create(request, data: ClientCreateRequest) -> ClientCreatedResponse:
    return 201, create_client(data)

@client_v1_router.get("/", response=list[ClientListResponse])
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN]) 
def list(request):
    return list_clients()
