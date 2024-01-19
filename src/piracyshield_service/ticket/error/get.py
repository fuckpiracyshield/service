from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.error.storage import TicketErrorStorage, TicketErrorStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketErrorGetService(BaseService):

    """
    Returns an error ticket.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_error_id: str) -> dict | Exception:
        """
        :param ticket_error_id: a valid ticket error identifier.
        :return: the error ticket document.
        """

        try:
            response = self.data_storage.get(
                ticket_error_id = ticket_error_id
            )

            if response.empty():
                self.logger.debug(f'Could not get error ticket for `{ticket_error_id}`')

            document = next(response, None)

            return document

        except TicketStorageGetException as e:
            self.logger.error(f'Could not get ticket for `{ticket_error_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketErrorStorage()
