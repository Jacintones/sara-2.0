


from ninja import Router

from apps.fonar.repository.fonar_repository import FonarRepository
from apps.fonar.service.fonar_service import FonarService
from apps.fonar.dto.fonar_dto import FormularioCreateRequest, FormularioCreatedResponse


router = Router(tags=["Fonar"])
fonar_repository = FonarRepository()
fonar_service = FonarService(fonar_repository)


@router.post("/", response={201: FormularioCreatedResponse, 400: dict, 403: dict})
def criar_formulario(request, data: FormularioCreateRequest):
    return fonar_service.criar_formulario(data)
