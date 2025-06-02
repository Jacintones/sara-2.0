import uuid
from ninja.errors import HttpError
from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.repository.license_repository import LicenseRepository
from apps.base.repository.client_repository import ClientRepository
from apps.base.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.base.entity.license import License


class LicenseService:
    """Serviço para operações com Licenças."""

    def __init__(self, repository: LicenseRepository, client_repository: ClientRepository):
        self.repository = repository
        self.client_repository = client_repository

    def create_license(self, data: LicenseCreateRequest) -> LicenseCreatedResponse:
        license_data = data.model_dump()
        client_id = license_data.pop("client_id")

        client_instance = self.client_repository.get_client_by_id(client_id)
        if not client_instance:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_CLIENT,
                status_code=404,
                message=f"Cliente com ID {client_id} não encontrado"
            )

        license = License(
            is_active=license_data.get("is_active", True),
            client=client_instance,
            key=uuid.uuid4()
        )

        self.repository.create_license(license)

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


