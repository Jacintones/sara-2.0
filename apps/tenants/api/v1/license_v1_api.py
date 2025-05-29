from ninja import Router
from apps.tenants.service.license_service import LicenseService
from apps.tenants.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse

license_v1_router = Router(tags=["Licenses"])
service = LicenseService()

@license_v1_router.post("/licenses", response=LicenseCreatedResponse)
def create_license(request, data: LicenseCreateRequest):
    return service.create_license(data)

@license_v1_router.get("/licenses", response=list[LicenseCreatedResponse])
def list_licenses(request):
    return service.list_licenses()
