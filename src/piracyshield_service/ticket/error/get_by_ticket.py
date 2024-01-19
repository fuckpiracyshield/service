from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.error.storage import TicketErrorStorage, TicketErrorStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketErrorGetByTicketService(BaseService):

    """
    Returns the error tickets by ticket identifier.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> list | Exception:
        """
        :param ticket_id: a valid ticket identifier.
        :return: list of error tickets identifiers.
        """

        try:
            response = self.data_storage.get_by_ticket(
                ticket_id = ticket_id
            )

            return list(response.batch())

        except TicketStorageGetException as e:
            self.logger.error(f'Could not get tickets for `{ticket_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketErrorStorage()
