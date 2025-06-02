from dependency_injector import containers, providers

from apps.base.repository.client_repository import ClientRepository
from apps.base.repository.license_repository import LicenseRepository
from apps.base.repository.user_repository import UserRepository
from apps.base.repository.victim_repository import VictimRepository
from apps.base.service.client_service import ClientService
from apps.base.service.license_service import LicenseService
from apps.base.service.user_service import UserService
from apps.base.service.victim_service import VictimService

class Container(containers.DeclarativeContainer):
    client_repository = providers.Factory(ClientRepository)
    license_repository = providers.Factory(LicenseRepository)
    victim_repository = providers.Factory(VictimRepository)
    user_repository = providers.Factory(UserRepository)

    client_service = providers.Singleton(
        ClientService,
        repository=client_repository
    )

    license_service = providers.Singleton(
        LicenseService,
        repository=license_repository,
        client_repository=client_repository
    )

    victim_service = providers.Singleton(
        VictimService,
        repository=victim_repository,
        license_repository=license_repository
    )

    user_service = providers.Singleton(
        UserService,
        repository=user_repository,
        client_repository=client_repository
    )
