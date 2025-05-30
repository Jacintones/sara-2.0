from utils.validators import BusinessValidator
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType


class DocumentValidationMixin:
    """Mixin para validação de documentos (CPF, CNPJ, RG, etc)."""
    
    def clean(self):
        super().clean()
        
        if hasattr(self, 'cnpj') and self.cnpj:
            if not BusinessValidator.validar_cnpj(self.cnpj):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_CNPJ,
                    status_code=400,
                    message='CNPJ inválido'
                )
                
        if hasattr(self, 'cpf') and self.cpf:
            if not BusinessValidator.validar_cpf(self.cpf):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_CPF,
                    status_code=400,
                    message='CPF inválido'
                )
                
        if hasattr(self, 'rg') and self.rg:
            if not BusinessValidator.validar_rg(self.rg):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_RG,
                    status_code=400,
                    message='RG inválido'
                )
                
        if hasattr(self, 'inscricao_estadual') and self.inscricao_estadual:
            if not BusinessValidator.validar_inscricao_estadual(self.inscricao_estadual, 'SP'):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_INSCRICAO_ESTADUAL,
                    status_code=400,
                    message='Inscrição Estadual inválida'
                )

class PersonValidationMixin:
    """Mixin para validação de dados pessoais (nome, email, etc)."""
    
    def clean(self):
        super().clean()
        
        if hasattr(self, 'nome') and self.nome:
            if not BusinessValidator.validar_nome(self.nome):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_NOME,
                    status_code=400,
                    message='Nome inválido'
                )
                
        if hasattr(self, 'email') and self.email:
            if not BusinessValidator.validar_email(self.email):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_EMAIL,
                    status_code=400,
                    message='Email inválido'
                )
                
        if hasattr(self, 'telefone') and self.telefone:
            if not BusinessValidator.validar_telefone(self.telefone):
                raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_TELEFONE,
                    status_code=400,
                    message='Telefone inválido'
                )
                
class AddressValidationMixin:
    """Mixin para validação de endereços."""
    
    def clean(self):
        super().clean()
        
        if hasattr(self, 'cep') and self.cep:
            if not BusinessValidator.validar_cep(self.cep):
                    raise ExceptionBase(
                    type_error=ErrorType.ERROR_INVALID_CEP,
                    status_code=400,
                    message='CEP inválido'
                )
                
                