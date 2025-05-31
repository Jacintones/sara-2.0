from ninja import Router
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse, TenantListResponse
from config.di import container

tenant_v1_router = Router(tags=["Tenants"])

@tenant_v1_router.post("/tenants", response=TenantCreatedResponse, auth=None)
def create_tenant(request, data: TenantCreateRequest):
    return container.tenant_service().create_tenant(data)

@tenant_v1_router.get("/tenants", response=list[TenantListResponse], auth=None)
def list_tenants(request):
    return container.tenant_service().list_tenants()

@tenant_v1_router.get("/tenants/{schema_name}", response=TenantListResponse, auth=None)
def get_tenant(request, schema_name: str):
    return container.tenant_service().get_tenant(schema_name)

