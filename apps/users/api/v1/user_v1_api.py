from django.http import HttpRequest
from ninja import Router
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse, UserResponse
from apps.users.service.user_service import UserService
from apps.users.repository.user_repository import UserRepository
from apps.users.enums.role_enum import RoleEnum
from config.core.auth.role_checker import check_role

router = Router(tags=["Users"])

repository = UserRepository()
service = UserService(repository=repository)

@router.post("/", response=UserCreateResponse)
@check_role([RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN])
def create_user(request, user_data: UserCreateRequest):
    return service.create_user(user_data)

@router.get("/{user_id}", response=UserResponse)
@check_role([RoleEnum.ADMIN, RoleEnum.USER])
def get_user(request: HttpRequest, user_id: int) -> UserResponse:
    return service.get_user(user_id)


@router.put("/{user_id}/activate", response=UserResponse, auth=None)
def activate_user(request: HttpRequest, user_id: int) -> UserResponse:
    return service.verify_user(user_id)




