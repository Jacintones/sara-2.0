from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from config.settings import base
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from typing import Dict, Optional
from ninja.security import HttpBearer

SECRET_KEY = base.JWT_SECRET_KEY
ALGORITHM = base.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = base.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[dict]:
        """
        Autentica o token JWT.
        """
        try:
            return verify_token(token)
        except Exception:
            raise ExceptionBase(
                type_error=ErrorType.UNAUTHORIZED_ERROR,
                status_code=401,
                message="Acesso não autorizado."
            )

    def get_missing_token_error(self):
        """Retorna o erro quando não há token."""
        return ExceptionBase(
            type_error=ErrorType.UNAUTHORIZED_ERROR,
            status_code=401,
            message="Token não fornecido. Por favor, faça login."
        )

def create_access_token(
    data: Dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT.
    """
    to_encode = data.copy()
    
    if expires_delta is None:
        expires_delta = timedelta(days=1)
        
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=30))
    to_encode.update({
        "exp": expire,
        "type": "refresh"  
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_type="access"):
    try:
        payload = jwt.decode(token, base.JWT_SECRET_KEY, algorithms=[base.JWT_ALGORITHM])
        if payload.get("type", "access") != expected_type:
            return None
        return payload
    except JWTError:
        raise ExceptionBase(
            type_error=ErrorType.INVALID_TOKEN,
            status_code=401
        )
