from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.security.anti_brute_force.memory import SecurityAntiBruteForceMemory, SecurityAntiBruteForceMemorySetException, SecurityAntiBruteForceMemoryGetException

from piracyshield_service.security.blacklist.add_ip_address import SecurityBlacklistAddIPAddressService

from piracyshield_service.security.errors import SecurityErrorCode, SecurityErrorMessage

class SecurityAntiBruteForceService(BaseService):

    """
    Protection against authentication flooding.
    """

    security_blacklist_add_ip_address_service = None

    anti_brute_force_config = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, email: str, ip_address: str) -> bool | Exception:
        login_attempts = self.data_memory.get_login_attempts(email = email)

        # we don't have any record, let's start monitoring
        if not isinstance(login_attempts, int) or login_attempts == 0:
            self.data_memory.set_login_attempts(
                email = email,
                timeframe = self.anti_brute_force_config.get('general').get('timeframe')
            )

        # we already have a count ongoing
        else:
            # the account has exceeded the maximum authentication attempts
            if login_attempts > self.anti_brute_force_config.get('general').get('max_attempts'):
                # remove any data as we're going to blacklist the IP
                self.data_memory.reset_login_attempts(email)

                self.logger.warning(f"Authentication limit reached by `{email}`")

                # create a blacklisting the IP address
                self.security_blacklist_add_ip_address_service.execute(
                    ip_address = ip_address,
                    duration = self.anti_brute_force_config.get('general').get('blacklist_duration')
                )

                raise ApplicationException(SecurityErrorCode.MAX_LOGIN_ATTEMPTS, SecurityErrorMessage.MAX_LOGIN_ATTEMPTS.format(self.anti_brute_force_config.get('general').get('blacklist_duration')))

            # increase the requests count until the maximum attempts limit is triggered
            else:
                self.data_memory.increment_login_attempts(
                    email = email
                )

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.anti_brute_force_config = Config('security/anti_brute_force')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_memory = SecurityAntiBruteForceMemory(
            database = self.anti_brute_force_config.get('database').get('memory_database')
        )

        self.security_blacklist_add_ip_address_service = SecurityBlacklistAddIPAddressService()
