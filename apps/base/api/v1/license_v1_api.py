from ninja import Router
from apps.base.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.base.di import container
from apps.accounts.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum

license_v1_router = Router(tags=["Licenses"])

@license_v1_router.post("/licenses", response={201: LicenseCreatedResponse, 400: dict, 403: dict})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_license(request, data: LicenseCreateRequest):
    return 201, container.license_service().create_license(data)


@license_v1_router.get("/licenses", response={200: list[LicenseCreatedResponse], 403: dict})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def list_licenses(request):
    return container.license_service().list_licenses()
