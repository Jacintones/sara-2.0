from enum import Enum

class RoleEnum(str, Enum):
    """Enum para os roles do sistema."""
    SUPER_ADMIN = "SUPER_ADMIN" 
    ADMIN = "ADMIN"              
    USER = "USER"                
    
    @classmethod
    def has_role(cls, user, role) -> bool:
        """
        Verifica se o usuário tem o role especificado.
        
        Hierarquia:
        - SUPER_ADMIN: Acesso total (desenvolvedores, suporte)
        - ADMIN: Administrador da instituição (coordenadores, gestores)
        - USER: Usuário comum (servidores, colaboradores)
        """
        if user.is_superuser:
            return True
            
        if role == cls.ADMIN:
            return user.is_staff
            
        if role == cls.USER:
            return True
            
        return False  