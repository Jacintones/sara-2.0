from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    access_token: str
    user_id: int
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    is_active: bool
    is_staff: bool
    is_superuser: bool
    redirect_url: Optional[str] = None 
    class Config:
        from_attributes = True 