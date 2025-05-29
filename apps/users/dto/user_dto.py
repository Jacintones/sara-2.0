from ninja import Schema
from pydantic import EmailStr

class UserCreateRequest(Schema):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    tenant_id: int | None


class UserDTO(Schema):
    """DTO para retornar dados do usuário."""
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    tenant_id: int | None
    is_verified: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserCreateResponse(UserDTO):
    """Response para criação de usuário."""
    pass 