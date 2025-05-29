
from ninja.errors import HttpError
from apps.tenants.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.tenants.models import License
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase


class LicenseService:

    @staticmethod
    def create_license(data: LicenseCreateRequest) -> LicenseCreatedResponse:
        try:
            license = License.objects.create(**data.model_dump())
            return LicenseCreatedResponse.model_validate(license)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_LICENSE,
                status_code=400,
                message=f"Erro ao criar licença: {str(e)}"
            )

    @staticmethod
    def list_licenses() -> list[LicenseCreatedResponse]:
        try:
            licenses = License.objects.all()
            return [LicenseCreatedResponse.model_validate(license) for license in licenses]
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_LICENSES,
                status_code=400,
                message=f"Erro ao listar licenças: {str(e)}"
            )

