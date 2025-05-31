from typing import List, Optional
from apps.victims.models import Victim
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType

class VictimRepository:
    """Repositório para operações com Vítimas."""
    
    def create_victim_from_dict(self, data: dict) -> Victim:
        """Cria uma nova vítima."""
        try:
            return Victim.objects.create(**data)
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao criar vítima",
                status_code=400,
                type_error=ErrorType.ERROR_CREATE_VICTIM,
            )
        
    def get_victim(self, victim_id: int) -> Optional[Victim]:
        """Obtém uma vítima pelo ID."""
        try:
            return Victim.objects.filter(id=victim_id).first()
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao buscar vítima",
                status_code=400,
                type_error=ErrorType.ERROR_GET_VICTIM,
            )
        
    def list_victims(self) -> List[Victim]:
        """Lista todas as vítimas."""
        try:
            return list(Victim.objects.all())
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao listar vítimas",
                status_code=400,
                type_error=ErrorType.ERROR_LIST_VICTIMS,
            )
        
    def update_victim(self, victim : Victim) -> Victim:
        """Atualiza os dados de uma vítima."""
        try:
            victim.save()
            return victim
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao atualizar vítima",
                status_code=400,
                type_error=ErrorType.ERROR_UPDATE_VICTIM,
            )
 
        
    def delete_victim(self, victim: Victim) -> None:
        """Exclui uma vítima."""
        try:
            victim.delete()
        except Exception as e:
            raise ExceptionBase(
                message="Erro ao excluir vítima",
                status_code=400,
                type_error=ErrorType.ERROR_DELETE_VICTIM,
            )