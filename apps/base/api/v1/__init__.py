from .license_v1_api import license_v1_router
from .client_v1_api import client_v1_router
from .user_v1_api import user_v1_router
from .victim_v1_api import victim_v1_router

__all__ = ["license_v1_router", "client_v1_router", "user_v1_router", "victim_v1_router"]
