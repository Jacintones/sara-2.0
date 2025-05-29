from typing import List, Optional
from apps.tenants.models import Tenant, Domain
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase

class TenantRepository:
    """Repositório para operações com Tenants."""
    
    def create_tenant(self, schema_name: str, name: str, paid_until=None, on_trial: bool = False) -> Tenant:
        """Cria um novo tenant."""
        try:
            tenant = Tenant.objects.create(
                schema_name=schema_name,
                name=name,
                paid_until=paid_until,
                on_trial=on_trial
            )
            return tenant
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_TENANT,
                status_code=400,
                message=f"Erro ao criar tenant: {str(e)}"
            )
        
    def create_domain(self, tenant: Tenant, domain: str, is_primary: bool = True) -> Domain:
        """Cria um novo domínio para o tenant."""
        try:
            return Domain.objects.create(
                tenant=tenant,
                domain=domain,
                is_primary=is_primary
            )
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_DOMAIN,
                status_code=400,
                message=f"Erro ao criar domínio: {str(e)}"
            )
        
    def get_tenant_by_schema(self, schema_name: str) -> Optional[Tenant]:
        """Obtém um tenant pelo schema_name."""
        try:
            return Tenant.objects.filter(schema_name=schema_name).first()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_TENANT,
                status_code=400,
                message=f"Erro ao buscar tenant: {str(e)}"
            )
        
    def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Obtém um tenant pelo domínio."""
        try:
            domain_obj = Domain.objects.filter(domain=domain).first()
            return domain_obj.tenant if domain_obj else None
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_TENANT,
                status_code=400,
                message=f"Erro ao buscar tenant: {str(e)}"
            )
        
    def list_tenants(self) -> List[Tenant]:
        """Lista todos os tenants."""
        try:
            return list(Tenant.objects.all())
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_TENANTS,
                status_code=400,
                message=f"Erro ao listar tenants: {str(e)}"
            )