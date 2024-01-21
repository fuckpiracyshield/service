from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.session.memory import AccountSessionMemory, AccountSessionMemorySetException, AccountSessionMemoryGetException

from piracyshield_service.account.session.get_current_by_account import AccountSessionGetCurrentByAccountService
from piracyshield_service.account.session.remove_long_session import AccountSessionRemoveLongSessionService
from piracyshield_service.account.session.remove_short_session import AccountSessionRemoveShortSessionService

from piracyshield_service.security.blacklist.add_refresh_token import SecurityBlacklistAddRefreshTokenService
from piracyshield_service.security.blacklist.add_access_token import SecurityBlacklistAddAccessTokenService

from dateutil.parser import parse

class AccountSessionDestroyCurrentSessionsService(BaseService):

    """
    Blacklists current sessions since we're logging out.
    """

    security_blacklist_add_access_token_service = None

    security_blacklist_add_refresh_token_service = None

    account_session_remove_short_session_service = None

    account_session_remove_long_session_service = None

    account_session_get_current_by_account_service = None

    session_config = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, account_id: str, current_access_token: str) -> bool | Exception:
        long_session, short_sessions = self.account_session_get_current_by_account_service.execute(
            account_id = account_id,
            current_access_token = current_access_token
        )

        now = Time.now()

        long_token_blacklist_delay = parse(long_session.get('expires_at')) - now

        long_token_blacklist_duration = round(long_token_blacklist_delay.total_seconds())

        self.security_blacklist_add_refresh_token_service.execute(
            refresh_token = long_session.get('token'),
            duration = long_token_blacklist_duration
        )

        self.account_session_remove_long_session_service.execute(
            account_id = account_id,
            refresh_token = long_session.get('token')
        )

        for short_session in short_sessions:
            short_token_blacklist_delay = parse(short_session.get('expires_at')) - now

            short_token_blacklist_duration = round(short_token_blacklist_delay.total_seconds())

            self.security_blacklist_add_access_token_service.execute(
                access_token = short_session.get('token'),
                duration = short_token_blacklist_duration
            )

            self.account_session_remove_short_session_service.execute(
                account_id = account_id,
                access_token = short_session.get('token')
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

        self.session_config = Config('security/session')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_memory = AccountSessionMemory(
            database = self.session_config.get('database').get('memory_database')
        )

        self.account_session_get_current_by_account_service = AccountSessionGetCurrentByAccountService()

        self.account_session_remove_long_session_service = AccountSessionRemoveLongSessionService()

        self.account_session_remove_short_session_service = AccountSessionRemoveShortSessionService()

        self.security_blacklist_add_refresh_token_service = SecurityBlacklistAddRefreshTokenService()

        self.security_blacklist_add_access_token_service = SecurityBlacklistAddAccessTokenService()
