from dependency_injector import containers, providers
from apps.tenants.repository.tenant_repository import TenantRepository
from apps.tenants.repository.license_repository import LicenseRepository
from apps.victims.repository.victim_repository import VictimRepository
from apps.tenants.service.tenant_service import TenantService
from apps.tenants.service.license_service import LicenseService
from apps.victims.service.victim_service import VictimService

class Container(containers.DeclarativeContainer):
    tenant_repository = providers.Factory(TenantRepository)
    license_repository = providers.Factory(LicenseRepository)
    victim_repository = providers.Factory(VictimRepository)

    tenant_service = providers.Singleton(
        TenantService,
        repository=tenant_repository
    )

    license_service = providers.Singleton(
        LicenseService,
        repository=license_repository,
        tenant_repository=tenant_repository
    )

    victim_service = providers.Singleton(
        VictimService,
        repository=victim_repository,
        license_repository=license_repository
    )
