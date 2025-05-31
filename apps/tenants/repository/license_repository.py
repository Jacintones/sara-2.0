from typing import List, Optional
from apps.tenants.models import License, Tenant

from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase

class LicenseRepository:
    """Repositório para operações com Licenças."""

    def create_license(self, license: License) -> License:
        """Cria uma nova licença."""
        try:
            license.save()
            return license
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_LICENSE,
                status_code=400,
                message=f"Erro ao criar licença: {str(e)}"
            )

    def get_license_by_key(self, key: str) -> Optional[License]:
        """Obtém uma licença pela chave."""
        try:
            return License.objects.filter(key=key).first()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_GET_LICENSE,
                status_code=400,
                message=f"Erro ao buscar licença: {str(e)}"
            )

    def list_licenses(self) -> List[License]:
        """Lista todas as licenças."""
        try:
            return list(License.objects.all())
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_LICENSES,
                status_code=400,
                message=f"Erro ao listar licenças: {str(e)}"
            )

    def update_license_status(self, license_id: int, is_active: bool) -> License:
        """Atualiza o status de uma licença."""
        try:
            license = License.objects.get(id=license_id)
            license.is_active = is_active
            license.save()
            return license
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_UPDATE_LICENSE,
                status_code=400,
                message=f"Erro ao atualizar licença: {str(e)}"
            )

    def delete_license(self, license_id: int) -> None:
        """Remove uma licença."""
        try:
            license = License.objects.get(id=license_id)
            license.delete()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_DELETE_LICENSE,
                status_code=400,
                message=f"Erro ao deletar licença: {str(e)}"
            )

