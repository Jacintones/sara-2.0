from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """DTO para requisição de login."""
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    """DTO para resposta de login."""
    access_token: str
    user_id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True 