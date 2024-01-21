from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.session.memory import AccountSessionMemory, AccountSessionMemorySetException, AccountSessionMemoryGetException

class AccountSessionGetCurrentByAccountService(BaseService):

    """
    Retrieves all the current sessions only.
    """

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
        # NOTE: have some optimizations in all of this.

        sessions = self.data_memory.get_all_short_by_account(
            account_id = account_id
        )

        long_session = None

        short_sessions = []

        # find the first short session to get back the long session
        for entry in sessions:
            (_, _, genre, token) = entry.split(':')

            # we found the current session
            if token in current_access_token:
                session = self.data_memory.get_session(entry)

                session['token'] = token

                short_sessions.append(session)

                # TODO: need to deal with this in the storage.
                # let's save the long session as well
                long_session = self.data_memory.get_session(f'session:{account_id}:long:{session.get('refresh_token')}')

                long_session['token'] = session.get('refresh_token')

                # avoid reappending the same session when we redo all of this
                sessions.remove(entry)

                break

        for entry in sessions:
            (_, _, genre, token) = entry.split(':')

            session = self.data_memory.get_session(entry)

            if session.get('refresh_token') == long_session.get('token'):
                session['token'] = token

                short_sessions.append(session)

        return (long_session, short_sessions)

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
