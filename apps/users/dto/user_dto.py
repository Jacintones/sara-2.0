from typing import Optional
from ninja import Schema
from pydantic import EmailStr

class UserCreateRequest(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_superuser: bool
    is_staff: bool
    tenant_id: int | None


class UserResponse(Schema):
    id: int
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


class UserCreateResponse(UserResponse):
    pass 

class UserUpdateRequest(Schema):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tenant_id: Optional[int] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None

    class Config:
        from_attributes = True