from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemGetAllStatusService(BaseService):

    """
    Returns the statuses of ticket items.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> list | Exception:
        try:
            response = self.data_storage.get_all_status(ticket_id)

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No ticket item found')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get the statuses of ticket items by ticket `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
