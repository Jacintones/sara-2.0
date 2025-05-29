from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """
    DTO para requisição de login.

    Attributes:
        email: Email do usuário
        password: Senha do usuário
        remember_me: Se verdadeiro, o token terá validade de 30 dias. Se falso, 1 dia.
    """
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    """
    DTO para resposta de login.

    Attributes:
        access_token: Token JWT para autenticação
        user_id: ID do usuário
        email: Email do usuário
        username: Nome de usuário
        first_name: Primeiro nome
        last_name: Sobrenome
        is_verified: Se o usuário está verificado
        is_active: Se o usuário está ativo
        is_staff: Se o usuário é staff
        is_superuser: Se o usuário é superusuário
    """
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