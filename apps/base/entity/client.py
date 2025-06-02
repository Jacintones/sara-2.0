import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):  
    name = models.CharField(_("Nome Fantasia"), max_length=100)
    razao_social = models.CharField(_("Razão Social"), max_length=255, default='')
    cnpj = models.CharField(_("CNPJ"), max_length=18, unique=True)
    endereco_comercial = models.CharField(_("Endereço Comercial"), max_length=255, default='')
    inscricao_estadual = models.CharField(_("Inscrição Estadual"), max_length=255, default='')
    nome_do_gestor = models.CharField(_("Nome do Gestor"), max_length=255, default='')
    rg_gestor = models.CharField(_("RG do Gestor"), max_length=20, default='', unique=True)
    cpf_gestor = models.CharField(_("CPF do Gestor"), max_length=14, default='', unique=True)
    endereco_residencial = models.CharField(_("Endereço Residencial"), max_length=255, default='')
    data_nascimento_gestor = models.DateField(_("Data de Nascimento do Gestor"), null=True, blank=True)
    cargo_gestor = models.CharField(_("Cargo do Gestor"), max_length=255, default='')
    unidade_executora = models.CharField(_("Unidade Executora"), max_length=255, default='')
    nome_responsavel = models.CharField(_("Nome do Responsável"), max_length=255, default='')
    funcao_responsavel = models.CharField(_("Função do Responsável"), max_length=255, default='')
    rg_responsavel = models.CharField(_("RG do Responsável"), max_length=20, default='', unique=True)
    cpf_responsavel = models.CharField(_("CPF do Responsável"), max_length=14, default='', unique=True)

    def __str__(self):
        return self.name
