from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageGetException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv4GetAllByProviderService(BaseService):

    """
    Returns all the IPv4 elements assigned to a provider.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, account_id: str) -> list | Exception:
        """
        Get all the IPv4 items in the database.

        :return
        """

        try:
            response = self.data_storage.get_all_items_with_genre_by_provider(
                genre = 'ipv4',
                provider_id = account_id
            )

            batch = response.batch()

            return list(batch)

        except TicketItemStorageGetException as e:
            self.logger.error(f'Could not get all the ticket IPv4s')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
