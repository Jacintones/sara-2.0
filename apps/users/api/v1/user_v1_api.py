from django.http import HttpRequest
from ninja import Router
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserDTO
from apps.users.service.user_service import UserService
from apps.users.repository.user_repository import UserRepository

router = Router(tags=["Users"])

repository = UserRepository()
service = UserService(repository=repository)

@router.post("/", response=UserCreateResponse)
def create_user(request, user_data: UserCreateRequest):
    """Cria um novo usuário."""
    return service.create_user(user_data)

@router.get("/{user_id}", response=UserDTO)
def get_user(request: HttpRequest, user_id: int) -> UserDTO:
    """Obtém um usuário pelo ID."""
    return service.get_user(user_id)

@router.get("/email/{email}", response=UserDTO)
def get_user_by_email(request: HttpRequest, email: str) -> UserDTO:
    """Obtém um usuário pelo email."""
    return service.get_user_by_email(email)
