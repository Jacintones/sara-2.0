

from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.dto.client_dto import ClientCreateRequest
from utils.validators import BusinessValidator


class ClientValidator:
    """
    Validates client data.
    """

    @staticmethod
    def validate_client_data(client_data: ClientCreateRequest) -> None:

        if not BusinessValidator.validate_cnpj(client_data.cnpj):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CNPJ,
                status_code=400,
                message="O CNPJ informado é inválido. Por favor, verifique se está correto.",
            )
        
        if not BusinessValidator.validate_cpf(client_data.cpf_gestor):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CPF,
                message="O CPF do gestor informado é inválido. Por favor, verifique se está correto.",
                status_code=400
            )
        
        if not BusinessValidator.validate_cpf(client_data.cpf_responsavel):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_CPF,
                status_code=400,
                message="O CPF do responsável informado é inválido. Por favor, verifique se está correto.",
            )
        
        if not BusinessValidator.validate_rg(client_data.rg_gestor):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_RG,
                status_code=400,
                message="O RG do gestor informado é inválido. Por favor, verifique se está correto.",
            )

        if not BusinessValidator.validate_rg(client_data.rg_responsavel):
            raise ExceptionBase(
                type_error=ErrorType.INVALID_RG,
                status_code=400,
                message="O RG do responsável informado é inválido. Por favor, verifique se está correto.",
            )