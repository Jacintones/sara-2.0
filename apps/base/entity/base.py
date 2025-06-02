import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        abstract = True