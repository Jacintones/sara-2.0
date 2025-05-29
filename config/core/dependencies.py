from typing import Dict, Any, TypeVar

T = TypeVar('T')

class DependencyContainer:
    """Container simples de dependências."""
    
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def register(cls, name: str, instance: Any) -> None:
        """Registra uma instância no container."""
        cls._instances[name] = instance
    
    @classmethod
    def get(cls, name: str) -> T:
        """Obtém uma instância do container."""
        if name not in cls._instances:
            raise KeyError(f"Dependência '{name}' não registrada.")
        return cls._instances[name]
    
    @classmethod
    def clear(cls) -> None:
        """Limpa todas as instâncias."""
        cls._instances.clear()


class Dependencies:
    """Interface para acessar dependências."""
    
    @staticmethod
    def get_repository(name: str) -> Any:
        return DependencyContainer.get(f"{name}_repository")
    
    @staticmethod
    def get_service(name: str) -> Any:
        return DependencyContainer.get(f"{name}_service")


dependencies = Dependencies()
