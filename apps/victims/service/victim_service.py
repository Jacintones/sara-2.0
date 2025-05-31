from typing import List
from apps.victims.repository.victim_repository import VictimRepository
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.victims.dto.victim_dto import (
    VictimCreateRequest, VictimCreateResponse, VictimResponse, 
    VictimUpdateRequest, VictimUpdateResponse
)
from apps.victims.validators.victim_validator import VictimValidator
from apps.tenants.repository.license_repository import LicenseRepository
from apps.victims.models import Victim
from config.core.mapper.mapper_schema import map_schema_to_model_dict

class VictimService:
    """Serviço para operações com Vítimas."""

    def __init__(self, repository: VictimRepository, license_repository: LicenseRepository):
        self.repository = repository
        self.license_repository = license_repository

    def create_victim(self, data: VictimCreateRequest) -> VictimCreateResponse:
        VictimValidator.validate_victim_creation(data)

        victim_dict = data.model_dump()
        license_key = victim_dict.pop("license_key", None)

        license = self.license_repository.get_license_by_key(license_key)
        if not license:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LICENSE_NOT_FOUND,
                status_code=404,
                message=f"Licença com chave {license_key} não encontrada"
            )
        if not license.is_active:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LICENSE_NOT_ACTIVE,
                status_code=400,
                message="Licença não está ativa"
            )

        victim = map_schema_to_model_dict(data, Victim)  
        license.is_active = False
        victim.license = license
        victim = self.repository.create_victim(victim, license)
        return VictimCreateResponse.model_validate(victim)


    def get_victim(self, victim_id: int) -> VictimResponse:
        """Obtém uma vítima pelo ID."""
        victim = self.repository.get_victim(victim_id)
        if not victim:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
                status_code=404,
                message=f"Vítima com ID {victim_id} não encontrada"
            )
        return VictimResponse.model_validate(victim)
        
    def list_victims(self) -> List[VictimResponse]:
        """Lista todas as vítimas."""
        victims = self.repository.list_victims()
        return [VictimResponse.model_validate(victim) for victim in victims]
            
    def update_victim(self, victim_id: int, data: VictimUpdateRequest) -> VictimResponse:
        """Atualiza uma vítima."""
        victim = self.repository.update_victim(victim_id, data)
        return VictimResponse.model_validate(victim)
            
    def delete_victim(self, victim_id: int) -> None:
        """Deleta uma vítima."""
        self.repository.delete_victim(victim_id)
