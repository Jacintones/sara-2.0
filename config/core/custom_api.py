from ninja import NinjaAPI
from ninja.errors import ValidationErrorContext, ValidationError
from typing import List, Dict, Any
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType


class CustomNinjaAPI(NinjaAPI):
    def validation_error_from_error_contexts(
        self, error_contexts: List[ValidationErrorContext],
    ) -> ValidationError:
        details: List[Dict[str, Any]] = []

        for context in error_contexts:
            for error in context.pydantic_validation_error.errors():
                field = ".".join(str(x) for x in error["loc"])
                error_type = error["type"]

                if error_type == "ausente":
                    message = f"O campo '{field}' é obrigatório."
                else:
                    message = error["msg"]

                details.append({
                    "field": field,
                    "message": message,
                    "type": error_type
                })

        exception = ExceptionBase(
            type_error=ErrorType.VALIDATION_ERROR,
            status_code=422,
            message="Erro de validação nos dados enviados",
            details=details
        )

        return ValidationError({
            "error": exception.type_error.value,
            "message": exception.message,
            "details": details
        })


