from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.session.memory import AccountSessionMemory, AccountSessionMemorySetException, AccountSessionMemoryGetException

class AccountSessionGetAllByAccountOrderedService(BaseService):

    """
    Retrieves all active sessions ordering them.
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

        sessions = self.data_memory.get_all_by_account(
            account_id = account_id
        )

        long_sessions = []
        short_sessions = []

        for entry in sessions:
            (_, _, genre, token) = entry.split(':')

            session = {
                'metadata': self.data_memory.get_session(entry)
            }

            if genre == 'long':
                session['long_session'] = token

                long_sessions.append(session)

            elif genre == 'short':
                session['short_session'] = token

                if token in current_access_token:
                    session['is_current'] = True

                short_sessions.append(session)

        for long_session in long_sessions:
            long_session['short_sessions'] = []

            for short_session in short_sessions:
                if short_session.get('metadata').get('refresh_token') == long_session.get('long_session'):
                    long_session['short_sessions'].append(short_session)

                    # if it's the currently used short session we can safely say that this is its long sessions
                    if short_session.get('is_current') == True:
                        long_session['is_current'] = True

        return {
            'long_sessions': long_sessions
        }

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
