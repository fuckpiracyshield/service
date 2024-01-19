from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketGetService(BaseService):

    """
    Ticket management class.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> bool | Exception:
        try:
            response = self.data_storage.get(ticket_id)

            if response.empty():
                self.logger.debug(f'No ticket found for `{ticket_id}`')

                raise ApplicationException(TicketErrorCode.TICKET_NOT_FOUND, TicketErrorMessage.TICKET_NOT_FOUND)

            document = next(response, None)

            return document

        except TicketStorageGetException as e:
            self.logger.error(f'Could not get ticket `{ticket_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketStorage()
