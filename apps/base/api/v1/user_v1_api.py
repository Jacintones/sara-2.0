from uuid import UUID
from django.http import HttpRequest
from ninja import Router
from apps.base.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest
from apps.base.enum.role_enum import RoleEnum
from apps.authenticate.auth.role_checker import check_role
from apps.base.core.exception.exception_base import ErrorResponse, ExceptionBase
from apps.base.service.user_service import create_user, get_user, update_user, verify_user
from apps.base.core.exception.error_type import ErrorType

user_v1_router = Router(tags=["Usuários"])

@user_v1_router.post("/", response={201: UserCreateResponse, 400: ErrorResponse, 403: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create(request, user_data: UserCreateRequest) -> UserCreateResponse:
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
    user = create_user(user_data)
    return 201, user

@user_v1_router.get("/{user_id}", response={200: UserResponse, 404: ErrorResponse})
@check_role([RoleEnum.ADMIN, RoleEnum.USER])
def get_by_id(request: HttpRequest, user_id: UUID) -> UserResponse:
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
    if not request.user.is_superuser and user_id != request.user.id:
        raise ExceptionBase(
            type_error=ErrorType.UNAUTHORIZED_ERROR,
            status_code=403,
            message="Você não tem permissão para acessar os dados deste usuário."
        )

    return get_user(user_id)

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
    return verify_user(user_id)


@user_v1_router.put("/{user_id}", response={200: UserResponse, 404: ErrorResponse, 400: ErrorResponse})
@check_role([RoleEnum.SUPER_ADMIN])
def update(request: HttpRequest, user_id: int, user_data: UserUpdateRequest) -> UserResponse:
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
    return update_user(user_id, user_data)
