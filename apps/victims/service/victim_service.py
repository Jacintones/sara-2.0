from typing import List
from apps.victims.repository.victim_repository import VictimRepository
from apps.victims.models import Victim
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from apps.victims.dto.victim_dto import (
    VictimCreateRequest, VictimCreateResponse, VictimResponse, 
    VictimUpdateRequest, VictimUpdateResponse
)
from apps.victims.validators.victim_validator import VictimValidator


class VictimService:
    """Serviço para operações com Vítimas."""
    
    def __init__(self, repository: VictimRepository):
        self.repository = repository
        
    def create_victim(self, victim_data: VictimCreateRequest) -> VictimCreateResponse:
        """
        Cria uma nova vítima.
        
        Args:
            victim_data: Dados da vítima
            
        Returns:
            VictimCreateResponse: Vítima criada
        """
        VictimValidator.validate_victim_creation(victim_data)

        data = victim_data.model_dump()
        victim = self.repository.create_victim(**data)
        return VictimCreateResponse.model_validate(victim)
            
    def get_victim(self, victim_id: int) -> VictimCreateResponse:
        """
        Obtém uma vítima pelo ID.
        
        Args:
            victim_id: ID da vítima
            
        Returns:
            VictimCreateResponse: Dados da vítima
            
        """
        victim = self.repository.get_victim(victim_id)
        if not victim:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
                status_code=404,
                message=f"Vítima não encontrada: {victim_id}"
            )
        return VictimCreateResponse.model_validate(victim)
        
    def list_victims(self) -> List[VictimResponse]:
        """
        Lista todas as vítimas.
        
        Returns:
            List[VictimCreateResponse]: Lista de vítimas
            
        Raises:
            ExceptionBase: Se houver erro ao listar
        """
        victims = self.repository.list_victims()
        return [VictimCreateResponse.model_validate(victim) for victim in victims]

            
    def update_victim(self, victim_id: int, victim_data: VictimUpdateRequest) -> VictimUpdateResponse:
        """
        Atualiza os dados de uma vítima existente.
        
        Args:
            victim_id: ID da vítima a ser atualizada
            victim_data: Novos dados da vítima
            
        Returns:
            VictimUpdateResponse: Vítima atualizada
            
        """
        VictimValidator.validate_victim_update(victim_data)
        
        victim = self.get_victim(victim_id)
        data = victim_data.model_dump(exclude_unset=True)
        
        for key, value in data.items():
            setattr(victim, key, value)
            
        updated_victim = self.repository.update_victim(victim)
        return VictimUpdateResponse.model_validate(updated_victim)
            
    def delete_victim(self, victim_id: int) -> None:
        """
        Exclui uma vítima.
        
        Args:
            victim_id: ID da vítima
            
        Raises:
            ExceptionBase: Se a vítima não for encontrada ou houver erro na exclusão
        """
        victim = self.get_victim(victim_id)
        self.repository.delete_victim(victim)
