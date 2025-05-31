import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from config.settings import base
from django.db import connection
from django_tenants.utils import get_public_schema_name

class Tenant(TenantMixin):  
    name = models.CharField(_("Nome"), max_length=100, null=False)
    razao_social = models.CharField(_("Razão Social"), max_length=255, default='', null=False)
    cnpj = models.CharField(_("CNPJ"), max_length=18, unique=True, null=False)
    endereco_comercial = models.CharField(_("Endereço Comercial"), max_length=255, default='', null=False)
    inscricao_estadual = models.CharField(_("Inscrição Estadual"), max_length=255, default='', null=False)
    nome_do_gestor = models.CharField(_("Nome do Gestor"), max_length=255, default='', null=False)
    rg_gestor = models.CharField(_("RG do Gestor"), max_length=20, default='', null=False, unique=True)
    cpf_gestor = models.CharField(_("CPF do Gestor"), max_length=14, default='', null=False, unique=True)
    endereco_residencial = models.CharField(_("Endereço Residencial"), max_length=255, default='', null=False)
    data_nascimento_gestor = models.DateField(_("Data de Nascimento do Gestor"), null=True, blank=True)
    cargo_gestor = models.CharField(_("Cargo do Gestor"), max_length=255, default='', null=False)
    unidade_executora = models.CharField(_("Unidade Executora"), max_length=255, default='', null=False)
    nome_responsavel = models.CharField(_("Nome do Responsável"), max_length=255, default='', null=False)
    funcao_responsavel = models.CharField(_("Função do Responsável"), max_length=255, default='', null=False)
    rg_responsavel = models.CharField(_("RG do Responsável"), max_length=20, default='', null=False, unique=True)
    cpf_responsavel = models.CharField(_("CPF do Responsável"), max_length=14, default='', null=False, unique=True)
    auto_create_schema = True  

class Domain(DomainMixin):
    pass

class TenantAwareManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        schema_name = connection.schema_name

        if schema_name is not get_public_schema_name():
            tenant = Tenant.objects.filter(schema_name=schema_name).first()
            return queryset.filter(tenant=tenant)
        else:
            return queryset


class License(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    tenant = models.ForeignKey(
        base.TENANT_MODEL,
        verbose_name=_("tenant"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    objects = TenantAwareManager()

