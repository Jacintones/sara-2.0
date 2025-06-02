from datetime import date
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from apps.base.dto.victim_dto import VictimCreateRequest, VictimUpdateRequest
from utils.validators import BusinessValidator


class VictimValidator:
    """Validador para operações com vítimas."""
    @staticmethod
    def validate_victim_creation(victim_data: VictimCreateRequest) -> None:
        """
        Valida os dados para criação de uma vítima.
        
        Args:
            victim_data: Dados da vítima a ser criada
            
        Raises:
            ExceptionBase: Se houver erro de validação
        """
        if not BusinessValidator.validate_cpf(victim_data.cpf):
            raise ExceptionBase(
                type_error=ErrorType.ERROR_INVALID_CPF,
                status_code=400,
                message="CPF inválido. Verifique se está correto."
            )

        if victim_data.birth_date > date.today():
            raise ExceptionBase(
                type_error=ErrorType.ERROR_INVALID_BIRTH_DATE,
                status_code=400,
                message="Data de nascimento não pode ser futura."
            )

        if not BusinessValidator.validate_cep(victim_data.postcode):
            raise ExceptionBase(
                type_error=ErrorType.ERROR_INVALID_POSTCODE,
                status_code=400,
                message="CEP inválido. Verifique se está correto."
            )

        if not BusinessValidator.validate_phone(victim_data.phone_number):
            raise ExceptionBase(
                type_error=ErrorType.ERROR_INVALID_PHONE,
                status_code=400,
                message="Telefone inválido. Verifique se está correto."
            )

    @staticmethod
    def validate_victim_update(victim_data: VictimUpdateRequest) -> None:
        """
        Valida os dados para atualização de uma vítima.
        
        Args:
            victim_data: Dados da vítima a ser atualizada
            
        Raises:
            ExceptionBase: Se houver erro de validação
        """
        data = victim_data.model_dump(exclude_unset=True)
        
        if "cpf" in data:
            if not BusinessValidator.validate_cpf(data["cpf"]):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_CPF,
                    status_code=400,
                    message="CPF inválido. Verifique se está correto."
                )

        if "birth_date" in data and data["birth_date"] > date.today():
            raise ExceptionBase(
                type_error=ErrorType.ERROR_INVALID_BIRTH_DATE,
                status_code=400,
                message="Data de nascimento não pode ser futura."
            )

        if "postcode" in data:
            if not BusinessValidator.validate_cep(data["postcode"]):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_POSTCODE,
                    status_code=400,
                    message="CEP inválido. Verifique se está correto."
                )

        if "phone_number" in data:
            if not BusinessValidator.validate_phone(data["phone_number"]):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_PHONE,
                    status_code=400,
                    message="Telefone inválido. Verifique se está correto."
                ) 