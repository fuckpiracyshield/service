from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketGetAllByProviderService(BaseService):

    """
    Returns only the tickets assigned to the specified provider account.
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
        :param account_id: the identifier of the account which created the tickets.
        :return: list of requested data.
        """

        try:
            response = self.data_storage.get_all_provider(account_id)

            if response.empty():
                self.logger.debug(f'No ticket found')

            return list(response.batch())

        except TicketStorageGetException as e:
            self.logger.error(f'Could not get tickets for `{account_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketStorage()
