from ninja import Router
from apps.users.dto.login_dto import LoginRequest, LoginResponse
from config.core.dependencies import dependencies

router = Router(tags=["Auth"])

@router.post("/login", response=LoginResponse)
def login(request, login_data: LoginRequest):
    return dependencies.get_service("auth").authenticate(login_data)


