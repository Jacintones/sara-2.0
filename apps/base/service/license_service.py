import uuid
from apps.base.dto.license_dto import LicenseCreateRequest, LicenseCreatedResponse
from apps.base.entity.license import License
from apps.base.entity.client import Client
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType


def create_license(data: LicenseCreateRequest) -> LicenseCreatedResponse:
    """Cria uma nova licença para um cliente existente."""
    try:
        license_data = data.model_dump()
        client_id = license_data.pop("client_id")

        try:
            client_instance = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_CLIENT,
                status_code=404,
                message=f"Cliente com ID {client_id} não encontrado"
            )

        license = License.objects.create(
            is_active=license_data.get("is_active", True),
            client=client_instance,
            key=uuid.uuid4()
        )

        return LicenseCreatedResponse.model_validate(license)
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.CLIENT_CREATION_ERROR,
            status_code=500,
            message="Erro ao criar licença.",
            details=str(e)
        )


def list_licenses() -> list[LicenseCreatedResponse]:
    """Lista todas as licenças."""
    try:
        licenses = License.objects.all()
        return [LicenseCreatedResponse.model_validate(lic) for lic in licenses]
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.CLIENT_LISTING_ERROR,
            status_code=500,
            message="Erro ao listar licenças.",
            details=str(e)
        )


def get_license_by_key(key: str) -> LicenseCreatedResponse:
    """Obtém uma licença pela chave."""
    try:
        license = License.objects.filter(key=key).first()
        if not license:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LICENSE_NOT_FOUND,
                status_code=404,
                message=f"Licença com chave {key} não encontrada"
            )
        return LicenseCreatedResponse.model_validate(license)
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.MAPPING_ERROR,
            status_code=500,
            message="Erro ao buscar licença pela chave.",
            details=str(e)
        )


def update_license_status(license_id: int, is_active: bool) -> LicenseCreatedResponse:
    """Atualiza o status de uma licença."""
    try:
        license = License.objects.filter(id=license_id).first()
        if not license:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LICENSE_NOT_FOUND,
                status_code=404,
                message=f"Licença com ID {license_id} não encontrada"
            )

        license.is_active = is_active
        license.save()

        return LicenseCreatedResponse.model_validate(license)
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.CLIENT_CREATION_ERROR,
            status_code=500,
            message="Erro ao atualizar status da licença.",
            details=str(e)
        )
