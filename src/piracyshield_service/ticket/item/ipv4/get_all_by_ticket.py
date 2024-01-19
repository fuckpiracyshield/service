from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv4GetAllByTicketService(BaseService):

    """
    Returns the IPv4 list of a ticket.
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
        Get all the IPv4 items by ticket_id.

        :return
        """

        try:
            response = self.data_storage.get_all_items_with_genre_by_ticket(
                ticket_id = ticket_id,
                genre = 'ipv4'
            )

            batch = response.batch()

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get all the IPv4 items for ticket `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
