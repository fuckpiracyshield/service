from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class WhitelistExistsByValueService(BaseService):

    """
    Check if a whitelist item exist.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, value: str) -> bool | Exception:
        try:
            response = self.data_storage.exists_by_value(
                value = value
            )

            batch = response.batch()

            if len(batch):
                return True

            return False

        except WhitelistStorageGetException as e:
            self.logger.error(f'Cannot find whitelist item `{item}`')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = WhitelistStorage()
