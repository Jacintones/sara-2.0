from enum import Enum

class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    INVALID_TOKEN = "invalid_token"
    INVALID_CREDENTIALS = "Credênciais inválidas"
    EMAIL_NOT_FOUND = "E-mail não encontrado"
    NOT_FOUND_ERROR = "not_found_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    UNAUTHORIZED_ERROR = "Acesso não autorizado"
    ERROR_CREATE_TENANT = "Erro ao criar tenant"
    ERROR_CREATE_DOMAIN = "Erro ao criar domínio"
    ERROR_GET_TENANT = "Erro ao buscar tenant"
    ERROR_UPDATE_TENANT = "Erro ao atualizar tenant"
    ERROR_DELETE_TENANT = "Erro ao excluir tenant"
    ERROR_LIST_TENANTS = "Erro ao listar tenants"
    ERROR_TENANT_NOT_FOUND = "Tenant não encontrado"
    ERROR_CREATE_USER = "Erro ao criar usuário"
    ERROR_GET_USER = "Erro ao buscar usuário"
    TENANT_NOT_FOUND = "Tenant não encontrado"
    ERROR_LOGIN = "Erro ao realizar login"
    INACTIVE_USER = "Usuário inativo"
    INVALID_TENANT = "Tenant inválido"
    INTEGRTY_ERROR = "Erro de integridade no banco de dados"
    ERROR_UPDATE_USER = "Erro ao atualizar usuário"
    # region License
    ERROR_CREATE_LICENSE = "Erro ao criar licença"
    ERROR_LIST_LICENSES = "Erro ao listar licenças"
    ERROR_GET_LICENSE = "Erro ao buscar licença"
    ERROR_UPDATE_LICENSE = "Erro ao atualizar licença"
    ERROR_DELETE_LICENSE = "Erro ao deletar licença"
    # endregion License
    # region Victim
    ERROR_CREATE_VICTIM = "Erro ao criar vítima"
    ERROR_UPDATE_VICTIM = "Erro ao atualizar vítima"
    ERROR_DELETE_VICTIM = "Erro ao excluir vítima"
    ERROR_LIST_VICTIMS = "Erro ao listar vítimas"
    ERROR_VICTIM_NOT_FOUND = "Vítima não encontrada"
    # endregion Victim

    
