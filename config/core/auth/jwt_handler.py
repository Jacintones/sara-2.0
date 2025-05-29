from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from config.settings import base
from config.core.exception.exception_base import ExceptionBase
from config.core.exception.error_type import ErrorType
from typing import Dict, Optional

SECRET_KEY = base.JWT_SECRET_KEY
ALGORITHM = base.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = base.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(
    data: Dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT.

    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração do token. Se None, usa 1 dia.

    Returns:
        str: Token JWT
    """
    to_encode = data.copy()
    
    # Se não foi passado tempo de expiração, usa 1 dia
    if expires_delta is None:
        expires_delta = timedelta(days=1)
        
    expire = datetime.utcnow() + expires_delta
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
