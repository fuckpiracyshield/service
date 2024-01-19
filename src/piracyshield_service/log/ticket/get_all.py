from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.log.ticket.storage import LogTicketStorage, LogTicketStorageGetException

from piracyshield_service.log.ticket.errors import LogTicketErrorCode, LogTicketErrorMessage

class LogTicketGetAllService(BaseService):

    """
    Gets all the logs of a ticket.
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
            response = self.data_storage.get_all(
                ticket_id = ticket_id
            )

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'Could not find any log for ticket `{ticket_id}`')

            return list(batch)

        except LogTicketStorageGetException as e:
            self.logger.error(f'Could not get all the logs for ticket `{ticket_id}`')

            raise ApplicationException(LogTicketErrorCode.GENERIC, LogTicketErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = LogTicketStorage()
