from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemGetDetailsService(BaseService):

    """
    Returns details needed to visualize the statistics of the ticket items.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, ticket_item_id: str) -> list | Exception:
        try:
            response = self.data_storage.get_details(ticket_id, ticket_item_id)

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No ticket item found')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get ticket item details for `{ticket_item_id}` by ticket `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
