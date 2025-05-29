from ninja import Router
from apps.users.dto.user_dto import UserCreateRequest, UserCreateResponse
from config.core.dependencies import dependencies

router = Router(tags=["Users"])

@router.post("/users", response=UserCreateResponse)
def create_user(request, user_data: UserCreateRequest):
    return dependencies.get_service("user").create_user(user_data)

@router.get("/users/{user_id}", response=UserCreateResponse)
def get_user(request, user_id: int):
    return dependencies.get_service("user").get_user(user_id)
