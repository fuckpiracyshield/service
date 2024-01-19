from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageUpdateException

from piracyshield_service.whitelist.errors import WhitelistErrorCode, WhitelistErrorMessage

class WhitelistSetStatusService(BaseService):

    """
    Sets the status of a whitelist item.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, item: str, status: bool) -> bool | Exception:
        try:
            affected_rows = self.data_storage.update_status(
                value = item,
                status = status
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not set the status for the whitelist item')

                raise ApplicationException(WhitelistErrorCode.CANNOT_SET_STATUS, WhitelistErrorMessage.CANNOT_SET_STATUS)

        except WhitelistStorageUpdateException as e:
            self.logger.error(f'Could not update the status of the whitelist item `{item}`')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = WhitelistStorage()
