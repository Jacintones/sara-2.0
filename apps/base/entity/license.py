import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.base.entity.client import Client

class License(models.Model):
    created = models.DateTimeField(_("Criado em"), auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(_("Está ativo"), default=True)

    client = models.ForeignKey(
        Client,
        verbose_name=_("Cliente"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Licença {self.key} - {'Ativa' if self.is_active else 'Inativa'}"
