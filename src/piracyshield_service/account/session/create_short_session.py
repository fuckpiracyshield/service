from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.session.memory import AccountSessionMemory, AccountSessionMemorySetException, AccountSessionMemoryGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

from datetime import timedelta

class AccountSessionCreateShortSessionService(BaseService):

    """
    Records a short session.
    """

    jwt_token_config = None

    session_config = None

    data_memory = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, refresh_token: str, access_token: str, account_id: str, ip_address: str) -> bool | Exception:
        # TODO: should we unpack the tokens and set their really real create and expire datetimes?

        now = Time.now()

        # short sessions could have been stored in a list, but because they all have different expire times,
        # and we don't want to expire them manually (automatically is something not yet possible in Redis),
        # we will store them in a string
        short_session_response = self.data_memory.add_short_session(
            account_id = account_id,
            refresh_token = refresh_token,
            access_token = access_token,
            data = {
                'refresh_token': refresh_token,
                'ip_address': ip_address,
                'created_at': str(now),
                'expires_at': str(now + timedelta(seconds = self.jwt_token_config.get('access_expiration_time')))
            },
            duration = self.jwt_token_config.get('access_expiration_time')
        )

        if not short_session_response:
            self.logger.error(f"Could not create a short session for `{account_id}`")

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC)

        self.logger.debug(f"Short session created for `{account_id}`")

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.session_config = Config('security/session')

        self.jwt_token_config = Config('security/token').get('jwt_token')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_memory = AccountSessionMemory(
            database = self.session_config.get('database').get('memory_database')
        )
