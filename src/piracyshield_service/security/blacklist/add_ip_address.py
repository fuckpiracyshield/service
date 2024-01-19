from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.security.blacklist.memory import SecurityBlacklistMemory, SecurityBlacklistMemorySetException, SecurityBlacklistMemoryGetException

from piracyshield_service.security.errors import SecurityErrorCode, SecurityErrorMessage

class SecurityBlacklistAddIPAddressService(BaseService):

    """
    Blacklists an IP address.
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

    def execute(self, ip_address: str, duration: int) -> bool | Exception:
        response = self.data_memory.add_ip_address(
            ip_address = ip_address,
            duration = duration
        )

        if response == True:
            self.logger.warning(f"Blacklist item `{ip_address}` has been added for {duration} seconds")

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
