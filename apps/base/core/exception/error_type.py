from enum import Enum

class ErrorType(Enum):
    # Erros de Autenticação e Autorização
    INVALID_TOKEN = "invalid_token"
    TOKEN_EXPIRED = "Token expirado"
    INVALID_CREDENTIALS = "Credênciais inválidas"
    NAME_NONE = "Nome é obrigatório"
    ERROR_LOGIN = "Erro ao fazer login"
    UNAUTHORIZED_ERROR = "Erro ao fazer login"
    MAPPING_ERROR = "Erro ao mapear schema para model"

    # Erros de Usuário
    EMAIL_NOT_FOUND = "E-mail não encontrado"
    INACTIVE_USER = "Usuário inativo"
    ERROR_CREATE_USER = "Erro ao criar usuário"
    ERROR_UPDATE_USER = "Erro ao atualizar usuário"
    INVALID_EMAIL = "Email inválido"
    INVALID_PASSWORD = "Senha inválida"
    USER_NOT_FOUND = "Usuário não encontrado"
    ERROR_GET_USER = "Erro ao buscar usuário"

    # Erros de cliente
    ERROR_CREATE_CLIENT = "Erro ao criar cliente"
    ERROR_GET_CLIENT = "Erro ao buscar cliente"
    ERROR_LIST_CLIENTS = "Erro ao listar clientes"
    ERROR_UPDATE_CLIENT = "Erro ao atualizar cliente"
    ERROR_DELETE_CLIENT = "Erro ao excluir cliente"

    # Erros de Validação
    VALIDATION_ERROR = "validation_error"
    INVALID_CNPJ = "CNPJ inválido"
    INVALID_CPF = "CPF inválido"
    INVALID_RG = "RG inválido"
    INTEGRTY_ERROR = "Erro de integridade no banco de dados"

    # Erros de Validação
    ERROR_CREATE_VICTIM = "Erro ao criar vítima"
    ERROR_GET_VICTIM = "Erro ao buscar vítima"
    ERROR_LIST_VICTIMS = "Erro ao listar vítimas"
    ERROR_UPDATE_VICTIM = "Erro ao atualizar vítima"
    ERROR_DELETE_VICTIM = "Erro ao excluir vítima"
    ERROR_INVALID_BIRTH_DATE = "Data de nascimento não pode ser futura"
    ERROR_INVALID_POSTCODE = "CEP inválido"
    ERROR_INVALID_PHONE = "Telefone inválido"
    ERROR_INVALID_CPF = "CPF inválido"
    ERROR_INVALID_RG = "RG inválido"
    
    # Erros de Licença
    ERROR_LICENSE_NOT_FOUND = "Licença não encontrada"
    ERROR_LICENSE_NOT_ACTIVE = "Licença não está ativa"
    ERROR_GET_LICENSE = "Erro ao buscar licença"
