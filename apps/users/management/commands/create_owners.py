from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

class Command(BaseCommand):
    help = "Cria usuários a partir do arquivo owners.txt"

    def handle(self, *args, **options):
        User = get_user_model()
        path = "owners.txt"  

        with open(path, "r") as f:
            for line in f:
                email = line.strip()
                if not email:
                    continue

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "is_superuser": True,
                        "is_staff": True,
                        "is_active": True,
                    }
                )

                if created:
                    user.set_password("SaraPortal@2025")  
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Usuário criado: {email}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Usuário já existe: {email}"))
