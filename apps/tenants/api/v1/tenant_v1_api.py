from ninja import Router
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse, TenantListResponse
from config.di import container
from apps.accounts.auth.role_checker import check_role
from apps.users.enums.role_enum import RoleEnum

tenant_v1_router = Router(tags=["Tenants"])

@tenant_v1_router.post("/tenants", response=TenantCreatedResponse, auth=None)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_tenant(request, data: TenantCreateRequest):
    return container.tenant_service().create_tenant(data), 201

@tenant_v1_router.get("/tenants", response=list[TenantListResponse], auth=None)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN]) 
def list_tenants(request):
    return container.tenant_service().list_tenants(), 200

@tenant_v1_router.get("/tenants/{schema_name}", response=TenantListResponse, auth=None)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def get_tenant(request, schema_name: str):
    return container.tenant_service().get_tenant(schema_name), 200

