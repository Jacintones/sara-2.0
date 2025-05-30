from ninja import Router
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse, TenantListResponse
from apps.tenants.service.tenant_service import TenantService
from apps.tenants.repository.tenant_repository import TenantRepository

tenant_v1_router = Router(tags=["Tenants"])

repository = TenantRepository()
service = TenantService(repository=repository)

@tenant_v1_router.post("/tenants", response=TenantCreatedResponse, auth=None)
def create_tenant(request, data: TenantCreateRequest):
    return service.create_tenant(data)

@tenant_v1_router.get("/tenants", response=list[TenantListResponse], auth=None)
def list_tenants(request):
    return service.list_tenants()

@tenant_v1_router.get("/tenants/{schema_name}", response=TenantListResponse, auth=None)
def get_tenant(request, schema_name: str):
    return service.get_tenant(schema_name)

