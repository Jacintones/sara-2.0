from jose import jwt
from django.utils.deprecation import MiddlewareMixin

from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from config.settings import base

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, base.JWT_SECRET_KEY, algorithms=[base.JWT_ALGORITHM])
                request.auth = payload
            except Exception as e:
                raise ExceptionBase(
                    message="Token inválido",
                    status_code=401,
                    type_error=ErrorType.UNAUTHORIZED_ERROR,
                    details=str(e)
                )
        else:
            request.auth = None
