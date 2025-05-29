from ninja import Router
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse
from apps.tenants.service.tenant_service import TenantService

tenant_v1_router = Router()  
service = TenantService()

@tenant_v1_router.post("/tenants", response=TenantCreatedResponse)
def create_tenant(request, data: TenantCreateRequest):
    return service.create_tenant(data)

@tenant_v1_router.get("/tenants", response=list[TenantCreatedResponse])
def list_tenants(request):
    return service.list_tenants()
