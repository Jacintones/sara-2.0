from typing import Optional
from uuid import UUID
from ninja import Schema
from pydantic import EmailStr

class UserCreateRequest(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_superuser: bool
    is_staff: bool
    client_id: UUID | None

class UserResponse(Schema):
    id: Optional[UUID] = None
    email: EmailStr
    first_name: str
    last_name: str
    client_id: UUID | None
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
    client_id: Optional[UUID] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None

    class Config:
        from_attributes = True