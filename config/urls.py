from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.urls import path, include
from ninja import NinjaAPI
from apps.tenants.api.v1 import tenant_v1_router, license_v1_router

api = NinjaAPI(
    version="1.0",
    title="Portal Sara API",
    docs_url="/docs",         # Swagger UI
    openapi_url="/openapi.json"  # JSON da especificação
)

api.add_router("/tenants", tenant_v1_router)
api.add_router("/licenses", license_v1_router)

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
