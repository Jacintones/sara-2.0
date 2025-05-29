import logging
from threading import local
from django.db import connection
from apps.tenants.models import Tenant
from django_tenants.utils import get_public_schema_name

logger = logging.getLogger(__name__)

_tenant_context = local()

def get_current_tenant() -> Tenant:
    """Retorna o tenant atual do contexto."""
    return getattr(_tenant_context, 'tenant', None)

def set_tenant_context(tenant: Tenant) -> None:
    """Define o tenant no contexto atual."""
    _tenant_context.tenant = tenant

def clear_tenant_context() -> None:
    """Limpa o contexto do tenant."""
    if hasattr(_tenant_context, 'tenant'):
        delattr(_tenant_context, 'tenant')

class TenantContextMiddleware:
    """
    Middleware para gerenciar o contexto do tenant.
    Integra com django-tenants e mantém o tenant atual em um contexto thread-safe.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        clear_tenant_context()
        
        try:
            schema_name = connection.schema_name
            
            if schema_name != get_public_schema_name():
                tenant = Tenant.objects.filter(schema_name=schema_name).first()
                if tenant:
                    set_tenant_context(tenant)
                    logger.debug(f"[TenantContext] Tenant definido: {tenant.name} ({schema_name})")
                else:
                    logger.warning(f"[TenantContext] Tenant não encontrado para schema: {schema_name}")
            
            response = self.get_response(request)
            return response
            
        except Exception as e:
            logger.exception(f"[TenantContext] Erro ao processar tenant: {str(e)}")
            raise
            
        finally:
            clear_tenant_context() 