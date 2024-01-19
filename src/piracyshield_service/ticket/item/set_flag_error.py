from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageUpdateException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemSetFlagErrorService(BaseService):

    """
    Flags a ticket item as error.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, value: str, status: bool) -> bool | Exception:
        """
        :param ticket_id: a valid ticket identifier.
        :param value: the value of the ticket item.
        :param: status: true or false if error or not.
        :return: true if everything is correct.
        """

        # TODO: validate status.

        try:
            affected_rows = self.data_storage.set_flag_error(
                ticket_id = ticket_id,
                value = value,
                status = status
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not set error flag for requested ticket item `{value}`, ticket `{ticket_id}`')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            # TODO: log operation.

            self.logger.debug(f'Ticket item error flag set to `{status}` for ticket item `{value}`, ticket `{ticket_id}`')

            return True

        except TicketItemStorageUpdateException as e:
            self.logger.error(f'Could not set error flag for requested ticket item `{value}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()
