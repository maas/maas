from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection

from maasapiserver.common.services._base import Service
from maasapiserver.v3.db.configurations import ConfigurationsRepository


class ConfigurationsService(Service):
    def __init__(
        self,
        connection: AsyncConnection,
        configurations_repository: ConfigurationsRepository | None = None,
    ):
        super().__init__(connection)
        self.configurations_repository = (
            configurations_repository
            if configurations_repository
            else ConfigurationsRepository(connection)
        )

    # We inherit this from the django legacy implementation. When we will have moved away, we can refactor the way we store the
    # configurations and provide a proper typing. For the time being, the consumer has to know how to consume the configuration.
    async def get(self, name: str) -> Any:
        configuration = await self.configurations_repository.get(name)
        if not configuration:
            return None
        return configuration.value
