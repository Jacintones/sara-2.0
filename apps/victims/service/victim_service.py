from typing import List
from apps.victims.repository.victim_repository import VictimRepository
from apps.victims.models import Victim
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

class VictimService:
    """Serviço para operações com Vítimas."""
    
    def __init__(self, repository: VictimRepository):
        self.repository = repository
        
    def create_victim(self, victim_data: dict, address_data: dict = None, contact_data: dict = None) -> Victim:
        """
        Cria uma nova vítima com endereço e contato opcionais.
        
        Args:
            victim_data: Dados da vítima
            address_data: Dados do endereço (opcional)
            contact_data: Dados do contato (opcional)
            
        Returns:
            Victim: Vítima criada
            
        Raises:
            ExceptionBase: Se houver erro na criação
        """
        try:
            # Cria a vítima
            victim = self.repository.create_victim(**victim_data)
            
            # Se fornecido, cria o endereço
            if address_data:
                self.repository.create_address(victim=victim, **address_data)
                
            # Se fornecido, cria o contato
            if contact_data:
                self.repository.create_contact(victim=victim, **contact_data)
                
            return victim
            
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_CREATE_VICTIM,
                status_code=400,
                message=f"Erro ao criar vítima: {str(e)}"
            )
            
    def get_victim(self, victim_id: int) -> Victim:
        """
        Obtém uma vítima pelo ID.
        
        Raises:
            ExceptionBase: Se a vítima não for encontrada
        """
        victim = self.repository.get_victim(victim_id)
        if not victim:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_VICTIM_NOT_FOUND,
                status_code=404,
                message=f"Vítima não encontrada: {victim_id}"
            )
        return victim
        
    def list_victims(self) -> List[Victim]:
        """Lista todas as vítimas."""
        try:
            return self.repository.list_victims()
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_LIST_VICTIMS,
                status_code=400,
                message=f"Erro ao listar vítimas: {str(e)}"
            )
            
    def update_victim(self, victim_id: int, victim_data: dict) -> Victim:
        """
        Atualiza os dados de uma vítima.
        
        Raises:
            ExceptionBase: Se a vítima não for encontrada ou houver erro na atualização
        """
        victim = self.get_victim(victim_id)
        try:
            return self.repository.update_victim(victim, **victim_data)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_UPDATE_VICTIM,
                status_code=400,
                message=f"Erro ao atualizar vítima: {str(e)}"
            )
            
    def delete_victim(self, victim_id: int) -> None:
        """
        Exclui uma vítima.
        
        Raises:
            ExceptionBase: Se a vítima não for encontrada ou houver erro na exclusão
        """
        victim = self.get_victim(victim_id)
        try:
            self.repository.delete_victim(victim)
        except Exception as e:
            raise ExceptionBase(
                type_error=ErrorType.ERROR_DELETE_VICTIM,
                status_code=400,
                message=f"Erro ao excluir vítima: {str(e)}"
            ) 