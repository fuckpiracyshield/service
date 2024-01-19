from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv6GetAllService(BaseService):

    """
    Returns all the tickets' IPv6 items.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self) -> dict | Exception:
        """
        Get all the IPv6 items in the database.

        :return
        """

        try:
            response = self.data_storage.get_all_items_with_genre(genre = 'ipv6')

            batch = response.batch()

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get all the ticket IPv6s')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
