from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.log.ticket.item.storage import LogTicketItemStorage, LogTicketItemStorageRemoveException

from piracyshield_service.log.ticket.item.errors import LogTicketItemErrorCode, LogTicketItemErrorMessage

class LogTicketItemRemoveAllService(BaseService):

    """
    Removes all the logs of a ticket item.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_item_id: str) -> bool | Exception:
        try:
            affected_rows = self.data_storage.remove_all(
                ticket_item_id = ticket_item_id
            )

            if not affected_rows:
                raise ApplicationException(LogTicketItemErrorCode.CANNOT_REMOVE, LogTicketItemErrorMessage.CANNOT_REMOVE)

            return True

        except LogTicketItemStorageRemoveException as e:
            self.logger.error(f'Could not remove all the logs for ticket item `{ticket_item_id}`')

            raise ApplicationException(LogTicketItemErrorCode.GENERIC, LogTicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = LogTicketItemStorage()
