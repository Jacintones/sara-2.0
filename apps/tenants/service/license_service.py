from ninja.errors import HttpError
from apps.tenants.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.tenants.models import License
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase
from apps.tenants.repository.license_repository import LicenseRepository


class LicenseService:
    """Serviço para operações com Licenças."""
    
    def __init__(self, repository: LicenseRepository):
        self.repository = repository

    def create_license(self, data: LicenseCreateRequest) -> LicenseCreatedResponse:
        """Cria uma nova licença."""
        license = self.repository.create_license(
            tenant_id=data.tenant_id,
            is_active=data.is_active
        )
        return LicenseCreatedResponse.model_validate(license)

    def list_licenses(self) -> list[LicenseCreatedResponse]:
        """Lista todas as licenças."""
        licenses = self.repository.list_licenses()
        return [LicenseCreatedResponse.model_validate(license) for license in licenses]

    def get_license_by_key(self, key: str) -> LicenseCreatedResponse:
        """Obtém uma licença pela chave."""
        license = self.repository.get_license_by_key(key)
        if not license:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LICENSE_NOT_FOUND,
                status_code=404,
                message=f"Licença com chave {key} não encontrada"
            )
        return LicenseCreatedResponse.model_validate(license)

    def update_license_status(self, license_id: int, is_active: bool) -> LicenseCreatedResponse:
        """Atualiza o status de uma licença."""
        license = self.repository.update_license_status(license_id, is_active)
        return LicenseCreatedResponse.model_validate(license)


