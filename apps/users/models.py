import uuid
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy 
from django.utils.translation import gettext_lazy as _
from config.settings import base

class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True, null=False)
    tenant = models.ForeignKey(
        base.TENANT_MODEL,
        verbose_name=_("tenant"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user has verified his email. "
        ),
    )

class EmailVerification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)