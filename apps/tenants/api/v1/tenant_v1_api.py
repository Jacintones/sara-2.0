from ninja import Router
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse, TenantListResponse
from config.di import container
from apps.accounts.auth.role_checker import check_role
from apps.users.enums.role_enum import RoleEnum
from config.core.exception.exception_base import ErrorResponse

tenant_v1_router = Router(tags=["Tenants"])

@tenant_v1_router.post("/", response={200: TenantCreatedResponse, 400: ErrorResponse, 403: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_tenant(request, data: TenantCreateRequest) -> TenantCreatedResponse:
    return container.tenant_service().create_tenant(data)


@tenant_v1_router.get("/tenants", response=list[TenantListResponse])
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN]) 
def list_tenants(request):
    return container.tenant_service().list_tenants()

@tenant_v1_router.get("/tenants/{schema_name}", response=TenantListResponse)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def get_tenant(request, schema_name: str):
    return container.tenant_service().get_tenant(schema_name)
