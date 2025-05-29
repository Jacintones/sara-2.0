
from ninja.errors import HttpError
from apps.tenants.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.tenants.models import License


class LicenseService:

    @staticmethod
    def create_license(data: LicenseCreateRequest) -> LicenseCreatedResponse:
        try:
            license = License.objects.create(**data.model_dump())
            return LicenseCreatedResponse.model_validate(license)
        except Exception as e:
            raise HttpError(400, f"Erro ao criar licença: {str(e)}")

    @staticmethod
    def list_licenses() -> list[LicenseCreatedResponse]:
        try:
            licenses = License.objects.all()
            return [LicenseCreatedResponse.model_validate(license) for license in licenses]
        except Exception as e:
            raise HttpError(500, f"Erro ao listar licenças: {str(e)}")

