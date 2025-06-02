from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from typing import Dict, Optional
from ninja.security import HttpBearer
from apps.base.entity.user import User
from apps.base.core.exception.exception_base import ExceptionBase
from apps.base.core.exception.error_type import ErrorType
from config.settings import base

SECRET_KEY = base.JWT_SECRET_KEY
ALGORITHM = base.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = base.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

logger = __import__('logging').getLogger(__name__)
    
class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[User]:
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")

            if not user_id:
                raise Exception("Token sem identificador de usuário.")

            logger.info(f"Autenticando usuário com ID: {user_id}")
            user = User.objects.get(id=user_id) 
            logger.info(f"Usuário encontrado: {user.email}")

            request.user = user 
            return user  
        except User.DoesNotExist:
            raise ExceptionBase(
                type_error=ErrorType.USER_NOT_FOUND,
                status_code=401,
                message="Usuário não encontrado."
            )
        except Exception:
            raise ExceptionBase(
                type_error=ErrorType.UNAUTHORIZED_ERROR,
                status_code=401,
                message="Acesso não autorizado."
            )


    def get_missing_token_error(self):
        return ExceptionBase(
            type_error=ErrorType.UNAUTHORIZED_ERROR,
            status_code=401,
            message="Token não fornecido. Por favor, faça login."
        )


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT com tempo de expiração e payload personalizado.
    """
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(days=1)

    expire = datetime.now(UTC) + expires_delta
    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de refresh com tipo 'refresh'.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=30))
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, expected_type: str = "access") -> Dict:
    """
    Decodifica e valida um token JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise JWTError("Tipo de token inválido.")
        return payload
    except JWTError:
        raise ExceptionBase(
            type_error=ErrorType.INVALID_TOKEN,
            status_code=401,
            message="Token inválido ou expirado."
        )
