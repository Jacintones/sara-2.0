from typing import List
from apps.tenants.repository.tenant_repository import TenantRepository
from apps.tenants.models import Tenant, Domain
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

class TenantService:
    """Serviço para operações com Tenants."""
    
    def __init__(self, repository: TenantRepository):
        self.repository = repository
        
    def create_tenant(self, schema_name: str, name: str, domain: str) -> Tenant:
        """
        Cria um novo tenant com seu domínio principal.
        """
        tenant = self.repository.create_tenant(
            schema_name=schema_name,
            name=name
        )
        self.repository.create_domain(
            tenant=tenant,
            domain=domain,
            is_primary=True
        )
        return tenant
        
            
    def list_tenants(self) -> List[Tenant]:
        """Lista todos os tenants."""
        return self.repository.list_tenants()

            
    def get_tenant(self, schema_name: str) -> Tenant:
        tenant = self.repository.get_tenant_by_schema(schema_name)
        if not tenant:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_TENANT_NOT_FOUND,
                status_code=404,
                message=f"Tenant com nome: {schema_name}, não encontrado"
            )
        return tenant

