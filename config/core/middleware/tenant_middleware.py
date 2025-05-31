import logging
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_tenant_model
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

logger = logging.getLogger(__name__)
TenantModel = get_tenant_model()

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'auth') or not request.auth:
            return
        
        logger.info("auth dentro do middleware de tenant : %s", request.auth)
        roles = request.auth.get("roles") or {}
        if roles.get("is_superuser"):
            request.tenant = None
            connection.set_schema_to_public()
            logger.info("Superusuário autenticado: sem tenant aplicado.")
            return


        tenant_schema = request.auth.get('tenant')
        if not tenant_schema:
            logger.error("Token não contém informação do tenant")
            raise ExceptionBase(
                message="Token inválido: tenant não especificado",
                status_code=401,
                type_error=ErrorType.UNAUTHORIZED_ERROR,
                details="Token não contém informação do tenant"
            )

        try:
            tenant = TenantModel.objects.get(schema_name=tenant_schema)
            connection.set_tenant(tenant)
            request.tenant = tenant
            logger.info(f"Tenant configurado: {tenant.name} (schema: {tenant_schema})")
        except TenantModel.DoesNotExist as e:
            logger.error(f"Tenant não encontrado: {tenant_schema}")
            raise ExceptionBase(
                message="Tenant não encontrado",
                status_code=404,
                type_error=ErrorType.TENANT_NOT_FOUND,
                details=str(e)
            )
        except Exception as e:
            logger.exception(f"Erro ao configurar tenant: {str(e)}")
            raise ExceptionBase(
                message="Erro ao configurar tenant",
                status_code=500,
                type_error=ErrorType.INTERNAL_ERROR,
                details=str(e)
            )
