from django.apps import AppConfig
from config.core.dependencies import DependencyContainer


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        """
        Chamado quando o app é inicializado.
        Registra manualmente as dependências.
        """
        from apps.users.repository.user_repository import UserRepository
        from apps.users.service.user_service import UserService
        from apps.users.service.auth_service import AuthService

        # Cria e registra o repository
        user_repository = UserRepository()
        DependencyContainer.register("user_repository", user_repository)

        # Cria e registra os services
        user_service = UserService(user_repository=user_repository)
        auth_service = AuthService(user_repository=user_repository)
        
        DependencyContainer.register("user_service", user_service)
        DependencyContainer.register("auth_service", auth_service)

