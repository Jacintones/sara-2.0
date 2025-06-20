import uuid
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy 
from django.utils.translation import gettext_lazy as _
from config.settings import base
from apps.base.manager.user_manager import CustomUserManager
from apps.base.entity.client import Client

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = None
    email = models.EmailField(_("email address"), blank=True, unique=True, null=False)
    client = models.ForeignKey(
        Client,
        verbose_name=_("client"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(
    _("email verified"),
    default=False,
    help_text=_("Indicates whether the user has confirmed their email address.")
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class EmailVerification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)