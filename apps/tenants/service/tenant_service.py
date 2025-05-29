from apps.tenants.models import Tenant
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse

class TenantService:

    @staticmethod
    def create_tenant(data: TenantCreateRequest) -> TenantCreatedResponse:
        tenant = Tenant.objects.create(**data.model_dump())
        return TenantCreatedResponse.model_validate(tenant)

    @staticmethod
    def list_tenants() -> list[TenantCreatedResponse]:
        tenants = Tenant.objects.all()
        return [TenantCreatedResponse.model_validate(t) for t in tenants]
