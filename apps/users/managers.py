from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from utils.validators import BusinessValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo de e-mail é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.full_clean()
        
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields["is_staff"]:
            raise ValueError("Superusuário precisa de is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superusuário precisa de is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
