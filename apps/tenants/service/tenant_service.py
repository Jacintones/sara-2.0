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
        
    @transaction.atomic
    def create_tenant(self, tenant_data: TenantCreateRequest) -> TenantCreatedResponse:
        self.validate_tenant(tenant_data)

        tenant_dict = tenant_data.model_dump()
        existing_tenant = self.repository.get_tenant_by_schema(tenant_dict['schema_name'])
        if existing_tenant:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_TENANT,
                status_code=400,
                message=f"Já existe tenant com schema_name: {tenant_dict['schema_name']}"
            )
            
        tenant = self.repository.create_tenant(tenant_dict)
        domain_name = f"{tenant.schema_name}.localhost"
        self.repository.create_domain(
            tenant=tenant,
            domain=domain_name,
            is_primary=True
        )

        return TenantCreatedResponse(
            id=tenant.id,
            name=tenant.name,
            cnpj=tenant.cnpj,
            nome_do_gestor=tenant.nome_do_gestor,
            data_nascimento_gestor=tenant.data_nascimento_gestor
        )
            
    def list_tenants(self) -> List[TenantListResponse]:
        tenants = self.repository.list_tenants()
        tenant_responses = []

        for tenant in tenants:
            domain_obj = self.repository.get_domain_by_schema(tenant.schema_name)
            domain_response = DomainResponse.model_validate(domain_obj) if domain_obj else None
            tenant_data = tenant.__dict__.copy()
            tenant_data.pop("_state", None)  

            tenant_response = TenantListResponse(
                **tenant_data,
                domain=domain_response
            )
            tenant_responses.append(tenant_response)
        return tenant_responses

    def get_domain_by_schema(self, schema_name: str) -> Domain:
        domain = self.repository.get_domain_by_schema(schema_name)
        if not domain:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_DOMAIN_NOT_FOUND,
                status_code=404,
                message=f"Domain com nome: {schema_name}, não encontrado"
            )
        
    def get_tenant(self, schema_name: str) -> TenantListResponse:
        tenant = self.repository.get_tenant_by_schema(schema_name)
        domain = self.repository.get_domain_by_schema(schema_name)
        if not tenant:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_TENANT_NOT_FOUND,
                status_code=404,
                message=f"Tenant com nome: {schema_name}, não encontrado"
            )
        domain_response = DomainResponse.model_validate(domain) if domain else None
        tenant_data = tenant.__dict__.copy()
        tenant_data.pop("_state", None)
        return TenantListResponse(
            **tenant_data,
            domain=domain_response
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
        
        

        


