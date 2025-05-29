from ninja import Router
from apps.users.dto.auth_dto import LoginRequest, LoginResponse
from apps.users.service.auth_service import AuthService
from apps.users.repository.user_repository import UserRepository

router = Router(tags=["Auth"])

repository = UserRepository()
service = AuthService(repository=repository)

@router.post("/login", response=LoginResponse, auth=None)
def login(request, login_data: LoginRequest):
    """Realiza o login do usuário."""
    return service.login(login_data)


