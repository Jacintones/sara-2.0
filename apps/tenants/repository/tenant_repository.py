from typing import List, Optional
from django.db import transaction
from apps.tenants.models import Tenant, Domain
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase

class TenantRepository:
    """Repositório para operações com Tenants."""

    def create_tenant(self, tenant: Tenant) -> Tenant:
        """Cria um novo tenant."""
        try:
            with transaction.atomic():
                tenant.save()
                self.create_domain(tenant, tenant.schema_name, is_primary=True)
            return tenant
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_TENANT,
                status_code=400,
                message=f"Erro ao criar tenant",
                details=str(e)
            )
        
    def create_domain(self, tenant: Tenant, domain: str, is_primary: bool = True) -> Domain:
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
                message=f"Erro ao criar domínio",
                details=str(e)
            )

    def get_tenant_by_schema(self, schema_name: str) -> Optional[Tenant]:
        """Obtém um tenant pelo schema_name."""
        try:
            return Tenant.objects.filter(schema_name=schema_name).first()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_TENANT,
                status_code=400,
                message=f"Erro ao buscar tenant",
                details=str(e)
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
                message=f"Erro ao buscar tenant",
                details=str(e)
            )

    def get_domain_by_schema(self, schema_name: str) -> Optional[Domain]:
        """Obtém um domínio pelo schema_name."""
        try:
            return Domain.objects.filter(tenant__schema_name=schema_name).first()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_DOMAIN,
                status_code=400,
                message=f"Erro ao buscar domínio",
                details=str(e)
            )

    def list_tenants(self) -> List[Tenant]:
        """Lista todos os tenants."""
        try:
            return list(Tenant.objects.all())
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_TENANTS,
                status_code=400,
                message=f"Erro ao listar tenants",
                details=str(e)
            )

    def get_tenant_by_id(self, tenant_id: int) -> Optional[Tenant]:
        """Obtém um tenant pelo id."""
        try:
            return Tenant.objects.get(id=tenant_id)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_TENANT,
                status_code=400,
                message=f"Erro ao buscar tenant",
                details=str(e)
            )
