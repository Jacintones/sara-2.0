from ninja import Router
from apps.tenants.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from config.di import container

license_v1_router = Router(tags=["Licenses"])

@license_v1_router.post("/licenses", response=LicenseCreatedResponse)
def create_license(request, data: LicenseCreateRequest):
    return container.license_service().create_license(data)


@license_v1_router.get("/licenses", response=list[LicenseCreatedResponse])
def list_licenses(request):
    return container.license_service().list_licenses()
