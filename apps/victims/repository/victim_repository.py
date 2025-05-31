from typing import List, Optional

from psycopg import Transaction
from apps.victims.models import Victim
from apps.tenants.models import License
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

class VictimRepository:
    """Repositório para operações com Vítimas."""


    def create_victim(self, victim: Victim, license: License) -> Victim:
        """Cria uma nova vítima e associa a licença de forma atômica."""
        try:
            with transaction.atomic():
                license.save()
                victim.save()
                return victim
        except Exception as e:
            logger.error(f"Erro ao criar vítima: {str(e)}", exc_info=True)
            raise ExceptionBase(
                message="Erro ao criar vítima",
                status_code=400,
                type_error=ErrorType.ERROR_CREATE_VICTIM,
                details=str(e)
            )

        
    def get_victim(self, victim_id: int) -> Optional[Victim]:
        """Obtém uma vítima pelo ID."""
        try:
            victim = Victim.objects.filter(id=victim_id).first()
            return victim
        except Exception as e:
            logger.error(f"Erro ao buscar vítima {victim_id}: {str(e)}", exc_info=True)
            raise ExceptionBase(
                message="Erro ao buscar vítima",
                status_code=400,
                type_error=ErrorType.ERROR_GET_VICTIM,
            )
        
    def list_victims(self) -> List[Victim]:
        """Lista todas as vítimas."""
        try:
            victims = list(Victim.objects.all())
            return victims
        except Exception as e:
            logger.error(f"Erro ao listar vítimas: {str(e)}", exc_info=True)
            raise ExceptionBase(
                message="Erro ao listar vítimas",
                status_code=400,
                type_error=ErrorType.ERROR_LIST_VICTIMS,
            )
        
    def update_victim(self, victim: Victim) -> Victim:
        """Atualiza os dados de uma vítima."""
        try:
            victim.save()
            return victim
        except Exception as e:
            logger.error(f"Erro ao atualizar vítima {victim.id}: {str(e)}", exc_info=True)
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
            logger.error(f"Erro ao excluir vítima {victim.id}: {str(e)}", exc_info=True)
            raise ExceptionBase(
                message="Erro ao excluir vítima",
                status_code=400,
                type_error=ErrorType.ERROR_DELETE_VICTIM,
            )