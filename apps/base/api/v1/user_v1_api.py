from django.http import HttpRequest
from ninja import Router
from apps.base.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.base.enum.role_enum import RoleEnum
from apps.accounts.auth.role_checker import check_role
from apps.base.core.exception.exception_base import ErrorResponse
from apps.base.di import container

user_v1_router = Router(tags=["Usuários"])

@user_v1_router.post("/", response={201: UserCreateResponse, 400: ErrorResponse, 403: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_user(request, user_data: UserCreateRequest) -> UserCreateResponse:
    """
    Cria um novo usuário no sistema.

    Args:
        user_data: Dados do usuário a ser criado

    Returns:
        201: Usuário criado com sucesso
        400: Erro de validação ou dados inválidos
        403: Sem permissão para criar usuário

    Example:
        ```json
        {
            "username": "novousuario",
            "first_name": "Novo",
            "last_name": "Usuário",
            "email": "novo@exemplo.com",
            "password": "senha123",
            "client_id": 1
        }
        ```

    Notes:
        - Requer permissão de SUPER_ADMIN ou ADMIN
        - O client_id é opcional
        - A senha será automaticamente criptografada
    """
    user = container.user_service.create_user(user_data)
    return 201, user

@user_v1_router.get("/{user_id}", response={200: UserResponse, 404: ErrorResponse})
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
    return container.user_service.get_user(user_id)

@user_v1_router.put("/{user_id}/activate", response={200: UserResponse, 404: ErrorResponse})
@check_role([RoleEnum.USER])
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
    return container.user_service.verify_user(user_id)


@user_v1_router.put("/{user_id}", response={200: UserResponse, 404: ErrorResponse, 400: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN])
def update_user(request: HttpRequest, user_id: int, user_data: UserUpdateRequest) -> UserResponse:
    """
    Atualiza os dados de um usuário existente.

    Args:
        user_id: ID do usuário a ser atualizado
        user_data: Novos dados do usuário

    Returns:
        200: Usuário atualizado com sucesso
        404: Usuário não encontrado
        400: Erro de validação

    Notes:
        - Requer permissão de ADMIN ou SUPER_ADMIN
        - Usuários normais só podem atualizar seus próprios dados
    """
    return container.user_service.update_user(user_id, user_data)
