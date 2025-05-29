from enum import Enum

class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    INVALID_TOKEN = "invalid_token"
    INVALID_CREDENTIALS = "Credênciais inválidas"
    EMAIL_NOT_FOUND = "E-mail não encontrado"
    NOT_FOUND_ERROR = "not_found_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    FORBIDDEN_ERROR = "forbidden_error"
    UNAUTHORIZED_ERROR = "unauthorized_error"
    ERROR_CREATE_LICENSE = "Erro ao criar licença"
    ERROR_LIST_LICENSES = "Erro ao listar licenças"
    ERROR_CREATE_TENANT = "Erro ao criar tenant"
    ERROR_LIST_TENANTS = "Erro ao listar tenants"
    ERROR_TENANT_NOT_FOUND = "Tenant não encontrado"
    ERROR_CREATE_USER = "Erro ao criar usuário"
    ERROR_GET_USER = "Erro ao buscar usuário"
    TENANT_NOT_FOUND = "Tenant não encontrado"
    ERROR_LOGIN = "Erro ao realizar login"
    INACTIVE_USER = "Usuário inativo"
    INVALID_TENANT = "Tenant inválido"

