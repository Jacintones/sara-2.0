from config.core.exception.error_type import ErrorType

class ExceptionBase(Exception):
    def __init__(self, type_error: ErrorType, status_code: int, message: str,details: list = None):
        self.titulo = type_error.value
        self.type_error = type_error  
        self.status_code = status_code
        self.message = message
        self.details = details or []

        super().__init__(self.message)  # ou apenas `message`
