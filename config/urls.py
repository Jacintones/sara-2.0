from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ninja.errors import ValidationError
from django.shortcuts import redirect
from django.urls import path, include
from psycopg import IntegrityError
from ninja import NinjaAPI
from ninja.errors import AuthenticationError

from apps.base.api.v1 import user_v1_router, client_v1_router, license_v1_router, victim_v1_router
from apps.accounts.api.v1 import auth_router
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from apps.accounts.auth.jwt_handler import JWTAuth

api = NinjaAPI(
    version="1.0",
    title="Portal Sara API",
    docs_url="/docs",         
    openapi_url="/openapi.json",
    auth=JWTAuth(),
)

api.add_router("/auth", auth_router)
api.add_router("/users", user_v1_router)
api.add_router("/clients", client_v1_router)
api.add_router("/licenses", license_v1_router)
api.add_router("/victims", victim_v1_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),  
    path("", lambda request: redirect("/api/v1/docs")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# region Exception Handler
@api.exception_handler(ExceptionBase)
def service_unavailable(request, exc: ExceptionBase):
    return api.create_response(
        request,
        {
            "title": exc.titulo,
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details
        },
        status=exc.status_code,
    )

@api.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    return api.create_response(
        request,
        {
            "title": ErrorType.INTEGRTY_ERROR,
            "message": "Erro de integridade no banco de dados. Verifique se as chaves estrangeiras existem.",
            "status_code": 400
        },
        status=400,
    )

@api.exception_handler(AuthenticationError)
def handle_authentication_error(request, exc):
    return api.create_response(
        request,
        {
            "title": ErrorType.UNAUTHORIZED_ERROR.value,
            "message": str(exc),
            "status_code": 401
        },
        status=401,
    )

@api.exception_handler(ValidationError)
def handle_validation_error(request, exc: ValidationError):
    validation_errors = exc.errors if hasattr(exc, "errors") else str(exc)
    return api.create_response(
        request,
        {
            "title": ErrorType.VALIDATION_ERROR.value,
            "message": "Erro de validação nos dados fornecidos.",
            "status_code": 422,
            "errors": validation_errors,  
        },
        status=422,
    )
# endregion