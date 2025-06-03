from typing import List
from uuid import UUID
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from apps.base.dto.victim_dto import (
    VictimCreateRequest, VictimCreateResponse, VictimResponse, 
    VictimUpdateRequest
)
from apps.base.entity.victim import Victim
from apps.base.entity.license import License
from apps.base.core.mapper.mapper_schema import map_schema_to_model_dict
from apps.base.validator.victim_validator import VictimValidator


def create_victim(data: VictimCreateRequest) -> VictimCreateResponse:
    VictimValidator.validate_victim_creation(data)

    license_key = data.license_key
    try:
        license = License.objects.get(key=license_key)
    except License.DoesNotExist:
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
    victim.license = license
    victim.save()

    license.is_active = False
    license.save()

    return VictimCreateResponse.model_validate(victim)


def get_victim(victim_id: int) -> VictimResponse:
    try:
        victim = Victim.objects.get(id=victim_id)
    except Victim.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
            status_code=404,
            message=f"Vítima com ID {victim_id} não encontrada"
        )
    return VictimResponse.model_validate(victim)


def list_victims() -> List[VictimResponse]:
    victims = Victim.objects.all()
    return [VictimResponse.model_validate(v) for v in victims]


def update_victim(victim_id: int, data: VictimUpdateRequest) -> VictimResponse:
    try:
        victim = Victim.objects.get(id=victim_id)
    except Victim.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
            status_code=404,
            message=f"Vítima com ID {victim_id} não encontrada"
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(victim, key, value)

    victim.save()
    return VictimResponse.model_validate(victim)


def delete_victim(victim_id: int) -> None:
    try:
        victim = Victim.objects.get(id=victim_id)
    except Victim.DoesNotExist:
        raise ExceptionBase(
            type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
            status_code=404,
            message=f"Vítima com ID {victim_id} não encontrada"
        )
    victim.delete()

def get_victims_by_client(client_id: UUID) -> List[VictimResponse]:
    victims = Victim.objects.filter(license__client_id=client_id)
    return [VictimResponse.model_validate(v) for v in victims] if victims else []