from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv4GetUnprocessedByTicketService(BaseService):

    """
    Returns the unprocessed IPv4 ticket items in a ticket.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, account_id: str) -> list | Exception:
        """
        Get all the unprocessed IPv4 items, of a specific ticket id, assigned to the account identifier.

        :param ticket_id: main ticket identifier.
        :param account_id: identifier of a provider.
        :return
        """

        try:
            response = self.data_storage.get_all_ticket_items_by(
                ticket_id = ticket_id,
                account_id = account_id,
                genre = TicketItemGenreModel.IPV4.value,
                status = TicketItemStatusModel.UNPROCESSED.value
            )

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No unprocessed IPv4 ticket item found for account `{account_id}`')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get all the procesed IPv4 items for ticket `{ticket_id}` for account `{account_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
