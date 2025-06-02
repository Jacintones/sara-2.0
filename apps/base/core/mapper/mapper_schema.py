from apps.base.core.exception.error_type import ErrorType
from apps.base.core.exception.exception_base import ExceptionBase


def map_schema_to_model_dict(schema_obj, model_cls):
    """
    Mapeia apenas os campos existentes do model Django, descartando extras do DTO,
    e retorna uma instância do model.
    """
    try:
        model_fields = set(f.name for f in model_cls._meta.get_fields())
        schema_dict = schema_obj.model_dump()
        filtered = {k: v for k, v in schema_dict.items() if k in model_fields}
        return model_cls(**filtered) 
    except Exception as e:
        raise ExceptionBase(
            type_error=ErrorType.MAPPING_ERROR,
            status_code=500,
            message="Erro ao mapear schema para model",
            details=str(e)
        )


