from django.http import HttpRequest
from ninja import Router
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse
from apps.users.service.user_service import UserService
from apps.users.repository.user_repository import UserRepository
from apps.users.enums.role_enum import RoleEnum
from apps.accounts.auth.role_checker import check_role

router = Router(tags=["Usuários"])

repository = UserRepository()
service = UserService(repository=repository)

@router.post("/", response={201: UserCreateResponse, 400: dict, 403: dict}, auth=None)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_user(request, user_data: UserCreateRequest):
    """
    Cria um novo usuário no sistema.

    Args:
        user_data: Dados do usuário a ser criado

    Returns:
        201: Usuário criado com sucesso
        400: Erro de validação ou tenant não encontrado
        403: Sem permissão para criar usuário

    Example:
        ```json
        {
            "username": "novousuario",
            "first_name": "Novo",
            "last_name": "Usuário",
            "email": "novo@exemplo.com",
            "password": "senha123",
            "tenant_id": 1
        }
        ```

    Notes:
        - Requer permissão de SUPER_ADMIN ou ADMIN
        - O tenant_id é opcional
        - A senha será automaticamente criptografada
    """
    return service.create_user(user_data)

@router.get("/{user_id}", response={200: UserResponse, 404: dict}, auth=None)
@check_role([RoleEnum.ADMIN, RoleEnum.USER])
def get_user(request: HttpRequest, user_id: int) -> UserResponse:
    """
    Obtém os dados de um usuário específico.

    Args:
        user_id: ID do usuário a ser consultado

    Returns:
        200: Dados do usuário
        404: Usuário não encontrado

    Notes:
        - Requer permissão de ADMIN ou USER
        - Usuários normais só podem ver seus próprios dados
        - Admins podem ver dados de qualquer usuário
    """
    return service.get_user(user_id)

@router.put("/{user_id}/activate", response={200: UserResponse, 404: dict}, auth=None)
def activate_user(request: HttpRequest, user_id: int) -> UserResponse:
    """
    Ativa um usuário no sistema.

    Args:
        user_id: ID do usuário a ser ativado

    Returns:
        200: Usuário ativado com sucesso
        404: Usuário não encontrado

    Notes:
        - Este endpoint não requer autenticação
        - Geralmente usado após confirmação de email
    """
    return service.verify_user(user_id)




