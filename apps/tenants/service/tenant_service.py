from typing import List, Optional
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.tenants.repository.tenant_repository import TenantRepository
from apps.tenants.models import Tenant, Domain
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.tenants.dto.tenant_dto import DomainResponse, TenantCreateRequest, TenantCreatedResponse, TenantListResponse
from utils.validators import BusinessValidator

class TenantService:    
    def __init__(self, repository: TenantRepository):
        self.repository = repository
        
    def create_tenant(self, data: TenantCreateRequest) -> TenantCreatedResponse:
        """Cria um novo tenant."""
        tenant = self.repository.create_tenant(data)
        return TenantCreatedResponse.model_validate(tenant)

    def list_tenants(self) -> list[TenantListResponse]:
        """Lista todos os tenants."""
        tenants = self.repository.list_tenants()
        return [TenantListResponse.model_validate(tenant) for tenant in tenants]

    def get_tenant(self, schema_name: str) -> TenantListResponse:
        """Obtém um tenant pelo schema_name."""
        tenant = self.repository.get_tenant_by_schema(schema_name)
        if not tenant:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_TENANT_NOT_FOUND,
                status_code=404,
                message=f"Tenant com schema {schema_name} não encontrado"
            )
        return TenantListResponse.model_validate(tenant)

    def get_domain_by_schema(self, schema_name: str) -> Domain:
        domain = self.repository.get_domain_by_schema(schema_name)
        if not domain:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_DOMAIN_NOT_FOUND,
                status_code=404,
                message=f"Domain com nome: {schema_name}, não encontrado"
            )
        
    def validate_tenant(self, tenant_data: TenantCreateRequest):
        if not BusinessValidator.validate_schema_name(tenant_data.schema_name):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_SCHEMA_NAME,
                status_code=400,
                message="Nome de esquema inválido."
            )
            
        if not BusinessValidator.validate_cnpj(tenant_data.cnpj):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CNPJ,
                status_code=400,
                message="O CNPJ informado é inválido."
            )

        if not BusinessValidator.validate_cpf(tenant_data.cpf_gestor):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CPF,
                status_code=400,
                message="CPF do gestor inválido."
            )
        
        if not BusinessValidator.validate_cpf(tenant_data.cpf_responsavel):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CPF,
                status_code=400,
                message="CPF do responsável inválido."
            )
        
        if not BusinessValidator.validate_rg(tenant_data.rg_gestor):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_RG,
                status_code=400,
                message="RG do gestor inválido."
            )
        
        

        


