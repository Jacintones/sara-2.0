from fonar.repository.fonar_repository import FonarRepository
from fonar.models import Formulario
from apps.fonar.dto.fonar_dto import FormularioCreateRequest, FormularioCreatedResponse
from config.core.exception.error_type import ErrorType
from config.core.exception.exception_base import ExceptionBase


class FonarService:
    def __init__(self, repository: FonarRepository):
        self.repository = repository

    def criar_formulario(self, data : FormularioCreateRequest) -> FormularioCreatedResponse:
        return self.repository.criar_formulario(data)

