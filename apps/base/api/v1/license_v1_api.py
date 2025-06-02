from ninja import Router
from apps.base.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.authenticate.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum
from apps.base.service.license_service import create_license, list_licenses

license_v1_router = Router(tags=["Licenses"])

@license_v1_router.post("/licenses", response={201: LicenseCreatedResponse, 400: dict, 403: dict})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create(request, data: LicenseCreateRequest):
    return 201, create_license(data)


@license_v1_router.get("/licenses", response={200: list[LicenseCreatedResponse], 403: dict})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def list_all(request):
    return list_licenses()
