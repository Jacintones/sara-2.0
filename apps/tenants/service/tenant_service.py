from apps.tenants.models import Tenant
from apps.tenants.dto.tenant_dto import TenantCreateRequest, TenantCreatedResponse

from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

class TenantService:

    @staticmethod
    def create_tenant(data: TenantCreateRequest) -> TenantCreatedResponse:
        try:
            tenant = Tenant.objects.create(**data.model_dump())
            return TenantCreatedResponse.model_validate(tenant)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.INTERNAL_SERVER_ERROR,
                status_code=500,
                message=f"Ocorreu um erro inesperado ao criar o tenant: {str(e)}"
            )

    @staticmethod
    def list_tenants() -> list[TenantCreatedResponse]:
        try:
            tenants = Tenant.objects.all()
            return [TenantCreatedResponse.model_validate(t) for t in tenants]
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.INTERNAL_SERVER_ERROR,
                status_code=500,
                message=f"Erro ao listar tenants: {str(e)}"
            )

