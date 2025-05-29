import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from apps.tenants.models import License

from .enums import (
    Gender, CivilStatus, Race, SexualOrientation,
    EducationLevel, Occupation, WorkStatus, Income,
    Children, Deficiency, DrugUsage, FederatedUnit, AggressionSource
)

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    class Meta:
        abstract = True

class Victim(BaseModel):
    license = models.OneToOneField("tenants.License", verbose_name=_("Licença"), on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(_('Nome'), max_length=48)
    social_name = models.CharField(_('Nome Social'), max_length=48, blank=True, null=True)
    cpf = models.CharField(_('CPF'), max_length=11)
    birth_date = models.DateField(_('Data de Nascimento (DD/MM/AAAA)'), max_length=60)
    postcode = models.CharField(_('CEP'), max_length=9)
    address = models.CharField(_('Endereço'), max_length=60)
    neighborhood = models.CharField(_('Bairro'), max_length=30)
    city = models.CharField(_('Cidade'), max_length=30)
    federated_unit = models.CharField(_('UF'), choices=FederatedUnit.choices, max_length=2)
    complement = models.CharField(_('Complemento'), max_length=60, blank=True, null=True)
    phone_number = models.CharField(_('Telefone'), max_length=60)
    civil_status = models.CharField(_('Estado Civil'), choices=CivilStatus.choices, max_length=1)
    spouse = models.CharField(_('Nome do Cônjuge'), max_length=60, blank=True, null=True)
    social_benefit = models.BooleanField(_('Benefício Social'))
    gender = models.CharField(_('Identidade de Gênero'), choices=Gender.choices, max_length=1)
    race = models.CharField(_('Raça'), choices=Race.choices, max_length=1)
    sexual_orientation = models.CharField(_('Orientação Sexual'), choices=SexualOrientation.choices, max_length=1)
    education = models.CharField(_('Escolaridade'), choices=EducationLevel.choices, max_length=4)
    occupation = models.CharField(_('Situação Ocupacional'), choices=Occupation.choices, max_length=4)
    profession = models.CharField(_('Ocupação/Profissão'), max_length=60)
    work_status = models.CharField(_('Situação Trabalhista'), choices=WorkStatus.choices, max_length=5)
    income = models.CharField(_('Renda'), choices=Income.choices, max_length=5)
    children = models.CharField(_('Total de Filhos'), choices=Children.choices, max_length=4)
    deficiency = models.CharField(_('Apresenta alguma deficiência/síndrome?'), choices=Deficiency.choices, max_length=2)
    deficiency_reason = models.BooleanField(_('Deficiência em decorrência da violência sofrida?'))
    has_consulted_psychiatrist = models.BooleanField(_('Já foi atendido por psiquiatra e/ou psicólogo?'))
    drug_usage = models.CharField(_('Faz uso de drogas ilícitas?'), choices=DrugUsage.choices, max_length=2)

class Aggression(models.Model):
    acknowledge = models.BooleanField(_('Confirmar'), default=False)
    type = models.CharField(
        choices=AggressionSource.choices,
        max_length=2
    )
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longitude'))
    victim = models.ForeignKey(
        Victim,
        on_delete=models.CASCADE
    )

class Phone(models.Model):
    victim = models.OneToOneField(verbose_name=_("Vítima"), to=Victim, on_delete=models.CASCADE)
    token = models.CharField(_("Token"), max_length=40, primary_key=True)

class PhoneActivation(BaseModel):
    victim = models.OneToOneField(verbose_name=_("Vítima"), to=Victim, on_delete=models.CASCADE)
    qr_code = models.CharField(_("QR Code"), max_length=40)

