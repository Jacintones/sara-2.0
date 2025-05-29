from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        """Inicializa o app."""
        # Importa o módulo de serviços para garantir que os singletons sejam criados
        from apps.users import service  # noqa

