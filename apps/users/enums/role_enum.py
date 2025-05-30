from enum import Enum

class RoleEnum(str, Enum):
    """Enum para os roles do sistema."""
    SUPER_ADMIN = "SUPER_ADMIN" 
    ADMIN = "ADMIN"              
    USER = "USER"                
    
    @classmethod
    def has_role(cls, user, role) -> bool:
        """
        Verifica se o usuário tem a role especificada.

        Hierarquia:
        - SUPER_ADMIN → tudo
        - ADMIN → ADMIN e USER
        - USER → apenas USER
        """
        if not hasattr(user, "is_authenticated") or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True 

        if role == cls.ADMIN:
            return user.is_staff

        if role == cls.USER:
            return True  

        return False
