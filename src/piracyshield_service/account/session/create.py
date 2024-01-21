from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.session.memory import AccountSessionMemory, AccountSessionMemorySetException, AccountSessionMemoryGetException

from piracyshield_service.account.session.create_long_session import AccountSessionCreateLongSessionService
from piracyshield_service.account.session.create_short_session import AccountSessionCreateShortSessionService

class AccountSessionCreateService(BaseService):

    """
    Records a session.

    We use the refresh token as the root of all the generated tokens, so we don't invalidate other ongoing sessions by saving them all indiscriminately.
    """

    account_session_create_short_session_service = None

    account_session_create_long_session_service = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, refresh_token: str, access_token: str, account_id: str, ip_address: str) -> bool | Exception:
        self.account_session_create_long_session_service.execute(
            refresh_token = refresh_token,
            access_token = access_token,
            account_id = account_id,
            ip_address = ip_address
        )

        self.account_session_create_short_session_service.execute(
            refresh_token = refresh_token,
            access_token = access_token,
            account_id = account_id,
            ip_address = ip_address
        )

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.account_session_create_long_session_service = AccountSessionCreateLongSessionService()

        self.account_session_create_short_session_service = AccountSessionCreateShortSessionService()
