from django.core.management.base import BaseCommand
from apps.tenants.models import Tenant, Domain
from django_tenants.utils import get_public_schema_name

class Command(BaseCommand):
    help = 'Inicializa o tenant público para desenvolvimento'

    def handle(self, *args, **options):
        if not Tenant.objects.filter(schema_name=get_public_schema_name()).exists():
            # Cria o tenant público
            public_tenant = Tenant.objects.create(
                name="Public",
                schema_name=get_public_schema_name(),
                # Preencha os campos obrigatórios do seu modelo Tenant
                razao_social="Public Tenant",
                cnpj="00.000.000/0000-00",
                endereco_comercial="Endereço Público",
                inscricao_estadual="Isento",
                nome_do_gestor="Admin",
                rg_gestor="0000000",
                cpf_gestor="000.000.000-00",
                endereco_residencial="Endereço Admin",
                cargo_gestor="Administrador",
                unidade_executora="Pública",
                nome_responsavel="Admin",
                funcao_responsavel="Administrador",
                rg_responsavel="0000000",
                cpf_responsavel="000.000.000-00"
            )

            # Cria os domínios para desenvolvimento local
            Domain.objects.create(
                domain='localhost',
                tenant=public_tenant,
                is_primary=True
            )
            Domain.objects.create(
                domain='127.0.0.1',
                tenant=public_tenant,
                is_primary=False
            )

            self.stdout.write(
                self.style.SUCCESS('Tenant público criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Tenant público já existe.')
            ) 