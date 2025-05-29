from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.urls import path, include
from psycopg import IntegrityError
from apps.tenants.api.v1 import tenant_v1_router, license_v1_router
from apps.users.api.v1 import auth_router, user_router
from config.core.exception.exception_base import ExceptionBase
from config.core.custom_api import CustomNinjaAPI

api = CustomNinjaAPI(
    version="1.0",
    title="Portal Sara API",
    docs_url="/docs",         
    openapi_url="/openapi.json",
)


api.add_router("/tenants", tenant_v1_router)
api.add_router("/licenses", license_v1_router)
api.add_router("/users", user_router)
api.add_router("/auth", auth_router)

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
            "type_error": exc.type_error,
            "message": exc.message,
            "status_code": exc.status_code
        },
        status=exc.status_code,
    )

@api.exception_handler(IntegrityError)
def handle_integrity_error(request, exc: IntegrityError):
    return api.create_response(
        request,
        {
            "type_error": "INTEGRITY_ERROR",
            "message": "Erro de integridade no banco de dados. Verifique se as chaves estrangeiras existem.",
            "details": str(exc),
            "status_code": 400
        },
        status=400,
    )
# endregion