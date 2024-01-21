from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.security.blacklist.memory import SecurityBlacklistMemory, SecurityBlacklistMemorySetException, SecurityBlacklistMemoryGetException

from piracyshield_service.security.errors import SecurityErrorCode, SecurityErrorMessage

class SecurityBlacklistAddAccessTokenService(BaseService):

    """
    Blacklists an access token.
    """

    blacklist_config = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, access_token: str, duration: int) -> bool | Exception:
        response = self.data_memory.add_access_token(
            access_token = access_token,
            duration = duration
        )

        if response == True:
            self.logger.warning(f"New access token has been blacklisted for {duration} seconds")

            return True

        return response

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.blacklist_config = Config('security/blacklist')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_memory = SecurityBlacklistMemory(
            database = self.blacklist_config.get('database').get('memory_database')
        )
