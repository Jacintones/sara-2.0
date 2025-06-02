from typing import Optional
from ninja import Schema
from pydantic import EmailStr

class LoginRequest(Schema):
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(Schema):
    access_token: str
    user_id: int
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool
    class Config:
        from_attributes = True 