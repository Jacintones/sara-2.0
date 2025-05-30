from django.db import models

class CustomTenantManager(models.Manager):
    def create(self, **kwargs):
        """
        Sobrescreve o método create para executar as validações antes de criar o objeto.
        """
        instance = self.model(**kwargs)
        instance.full_clean()
        instance.save(force_insert=True, using=self.db)
        return instance 