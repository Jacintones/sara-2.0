from enum import Enum

class ErrorType(Enum):
    # Erros de Autenticação e Autorização
    INVALID_TOKEN = "invalid_token"
    TOKEN_EXPIRED = "Token expirado"
    INVALID_CREDENTIALS = "Credênciais inválidas"
    UNAUTHORIZED = "Acesso não autorizado"
    
    # Erros de Usuário
    EMAIL_NOT_FOUND = "E-mail não encontrado"
    INACTIVE_USER = "Usuário inativo"
    ERROR_CREATE_USER = "Erro ao criar usuário"
    ERROR_UPDATE_USER = "Erro ao atualizar usuário"
    INVALID_EMAIL = "Email inválido"
    INVALID_PASSWORD = "Senha inválida"
    
    # Erros de Tenant
    ERROR_CREATE_TENANT = "Erro ao criar tenant"
    ERROR_CREATE_DOMAIN = "Erro ao criar domínio"
    TENANT_NOT_FOUND = "Tenant não encontrado"
    INVALID_TENANT = "Tenant inválido"
    INVALID_SCHEMA_NAME = "Nome de esquema inválido"
    ERROR_DOMAIN_NOT_FOUND = "Domain não encontrado"
    TENANT_REQUIRED = "Tenant obrigatório"

    # Erros de Validação
    VALIDATION_ERROR = "validation_error"
    INVALID_CNPJ = "CNPJ inválido"
    INVALID_CPF = "CPF inválido"
    INVALID_RG = "RG inválido"
    INTEGRTY_ERROR = "Erro de integridade no banco de dados"

    
