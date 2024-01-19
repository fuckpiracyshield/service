from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class WhitelistGetGlobalService(BaseService):

    """
    Get all the whitelist items.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self) -> list | Exception:
        try:
            response = self.data_storage.get_global()

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No whitelist item found')

            return list(batch)

        except WhitelistStorageGetException as e:
            self.logger.error(f'Cannot get all the whitelist items')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = WhitelistStorage()
