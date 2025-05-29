from ninja import Router
from apps.users.dto.auth_dto import LoginRequest, LoginResponse
from apps.users.service.auth_service import AuthService
from apps.users.repository.user_repository import UserRepository
from ninja.errors import AuthenticationError
from config.core.exception.error_type import ErrorType

router = Router(tags=["Autenticação"])

repository = UserRepository()
service = AuthService(repository=repository)

@router.post("/login", response={200: LoginResponse, 401: dict, 500: dict}, auth=None)
def login(request, login_data: LoginRequest):
    """
    Realiza o login do usuário e retorna um token JWT.

    Args:
        login_data: Dados de login (email, senha e remember_me)

    Returns:
        200: Token JWT e informações do usuário
        401: Erro de autenticação (credenciais inválidas)
        500: Erro interno do servidor

    Example:
        ```json
        {
            "email": "usuario@exemplo.com",
            "password": "senha123",
            "remember_me": true
        }
        ```
    
    Notes:
        - Se remember_me for true, o token terá validade de 30 dias
        - Se remember_me for false, o token terá validade de 1 dia
        - O token deve ser enviado no header Authorization como Bearer Token
    """
    return service.login(login_data)


