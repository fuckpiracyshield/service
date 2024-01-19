from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.log.ticket.storage import LogTicketStorage, LogTicketStorageRemoveException

from piracyshield_service.log.ticket.errors import LogTicketErrorCode, LogTicketErrorMessage

class LogTicketRemoveAllService(BaseService):

    """
    Removes all the logs of a ticket.
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
            affected_rows = self.data_storage.remove_all(
                ticket_id = ticket_id
            )

            if not affected_rows:
                raise ApplicationException(LogTicketErrorCode.CANNOT_REMOVE, LogTicketErrorMessage.CANNOT_REMOVE)

            return True

        except LogTicketStorageRemoveException as e:
            self.logger.error(f'Could not remove all the logs for ticket `{ticket_id}`')

            raise ApplicationException(LogTicketErrorCode.GENERIC, LogTicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = LogTicketStorage()
