from enum import Enum

class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND_ERROR = "not_found_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    FORBIDDEN_ERROR = "forbidden_error"
    UNAUTHORIZED_ERROR = "unauthorized_error"
    ERROR_CREATE_LICENSE = "Erro ao criar licença"
    ERROR_LIST_LICENSES = "Erro ao listar licenças"

