from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketGetTotalService(BaseService):

    """
    Returns the tickets count.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self) -> int | Exception:
        try:
            return self.data_storage.get_total()

        except TicketStorageGetException as e:
            self.logger.error(f'Could not get total count of tickets')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketStorage()
