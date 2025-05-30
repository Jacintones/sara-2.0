from django.db import connection
from django.conf import settings
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from config.settings import base
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase
import logging
from django.core.cache import cache
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

class MultiTenantAuthMiddleware:
    EXEMPT_URLS = [
        '/api/auth/login/',
        '/api/health/',
        '/api/docs/',
        '/api/v1/docs/**',
        '/api/v1/openapi.json',
        '/api/v1/schema',
        '/api/v1/auth/login',
        '/',
        '/admin/'
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_tenant_from_cache(self, user_id, tenant_id):
        """Verifica no cache se o usuário tem acesso ao tenant"""
        cache_key = f"user_tenant_{user_id}_{tenant_id}"
        return cache.get(cache_key)

    def _cache_tenant_access(self, user_id, tenant_id, has_access):
        """Armazena em cache o acesso do usuário ao tenant"""
        cache_key = f"user_tenant_{user_id}_{tenant_id}"
        cache.set(cache_key, has_access, timeout=3600)  

    def _validate_tenant_access(self, user_id, tenant_id):
        """Valida se o usuário tem acesso ao tenant específico"""
        try:
            user = User.objects.get(id=user_id)
            has_access = user.tenants.filter(id=tenant_id).exists()
            self._cache_tenant_access(user_id, tenant_id, has_access)
            return has_access
        except User.DoesNotExist:
            return False

    def __call__(self, request):
        if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return self.get_response(request)

        auth = request.headers.get("Authorization")
        if not auth:
            logger.warning(f"Tentativa de acesso sem token de autorização: {request.path}")
            raise ExceptionBase(
                type_error=ErrorType.INVALID_TOKEN,
                status_code=401,
                message="Token de autorização não fornecido."
            )

        if not auth.startswith("Bearer "):
            logger.warning(f"Formato de token inválido: {auth[:10]}...")
            raise ExceptionBase(
                type_error=ErrorType.INVALID_TOKEN,
                status_code=401,
                message="Formato de token inválido. Use 'Bearer <token>'."
            )

        token = auth.split(" ")[1]
        try:
            payload = jwt.decode(token, base.JWT_SECRET_KEY, algorithms=base.JWT_ALGORITHM)
            
            user_id = payload.get("user_id")
            tenant_from_token = payload.get("tenant")
            current_schema = connection.schema_name

            if not all([user_id, tenant_from_token]):
                logger.error("Token não contém informações necessárias (user_id ou tenant)")
                raise ExceptionBase(
                    type_error=ErrorType.INVALID_TOKEN,
                    status_code=401,
                    message="Token inválido: informações ausentes."
                )

            has_access = self._get_tenant_from_cache(user_id, tenant_from_token)
            
            if has_access is None:
                has_access = self._validate_tenant_access(user_id, tenant_from_token)

            if not has_access:
                logger.warning(f"Usuário {user_id} tentou acessar tenant não autorizado: {tenant_from_token}")
                raise ExceptionBase(
                    type_error=ErrorType.UNAUTHORIZED,
                    status_code=403,
                    message="Usuário não tem acesso a este tenant."
                )

            if tenant_from_token != current_schema:
                logger.warning(f"Tentativa de acesso com tenant inválido. Token: {tenant_from_token}, Schema: {current_schema}")
                raise ExceptionBase(
                    type_error=ErrorType.TENANT_NOT_FOUND,
                    status_code=401,
                    message="Tenant inválido para o token fornecido."
                )
            request.tenant_id = tenant_from_token
            request.user_id = user_id

        except ExpiredSignatureError:
            logger.warning("Token expirado recebido")
            raise ExceptionBase(
                type_error=ErrorType.TOKEN_EXPIRED,
                status_code=401,
                message="Token expirado."
            )
        except JWTError as e:
            logger.error(f"Erro ao decodificar token: {str(e)}")
            raise ExceptionBase(
                type_error=ErrorType.INVALID_TOKEN,
                status_code=401,
                message="Token inválido."
            )

        return self.get_response(request) 