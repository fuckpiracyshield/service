from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageRemoveException

from piracyshield_service.whitelist.errors import WhitelistErrorCode, WhitelistErrorMessage

class WhitelistRemoveService(BaseService):

    """
    Removes a whitelist item created by an account.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, value: str, account_id: str) -> None | Exception:
        try:
            affected_rows = self.data_storage.remove(
                value = value,
                account_id = account_id
            )

            if not affected_rows:
                raise ApplicationException(WhitelistErrorCode.CANNOT_REMOVE, WhitelistErrorMessage.CANNOT_REMOVE)

            # NOTE: should we consider a task to mark all the pre existent items as non whitelisted anymore?

        except WhitelistStorageRemoveException as e:
            self.logger.error(f'Cannot remove whitelist item `{value}`')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = WhitelistStorage()
