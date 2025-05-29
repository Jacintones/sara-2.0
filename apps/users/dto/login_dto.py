from ninja import Schema
from pydantic import EmailStr

class LoginRequest(Schema):
    email: EmailStr
    password: str
    remember_me: bool = False

class LoginResponse(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(Schema):
    refresh_token: str
