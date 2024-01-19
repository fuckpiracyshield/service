from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageGetException

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketExistsByIdentifierService(BaseService):

    """
    Checks if there's a ticket with this identifier.
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
            response = self.data_storage.exists_by_identifier(
                ticket_id = ticket_id
            )

            batch = response.batch()

            if len(batch):
                return True

            return False

        except TicketStorageGetException as e:
            self.logger.error(f'Could not verify if a ticket exists with the identifier `{ticket_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketStorage()
