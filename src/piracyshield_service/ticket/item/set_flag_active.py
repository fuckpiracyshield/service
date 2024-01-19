from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageUpdateException

from piracyshield_service.log.ticket.item.create import LogTicketItemCreateService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemSetFlagActiveService(BaseService):

    """
    Sets the flags as active or not.

    This removes the ticket item from the list of the ticket items to block by the providers.
    """

    log_ticket_item_create_service = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, internal_id: str, value: str, status: bool) -> bool | Exception:
        """
        Set the blocking activity status.
        This will exclude the ticket item from the list that any provider can get.

        :param internal_id: the associated internal id.
        :param value: the value of the ticket item.
        :param status: true/false if status is active or not.
        :return
        """

        # TODO: validate status.

        try:
            affected_rows = self.data_storage.set_flag_active(
                value = value,
                status = status
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not set active flag for requested ticket item `{value}`, requested by {internal_id}')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            # TODO: log operation.

            self.logger.debug(f'Ticket item active flag set to `{status}` for `{value}` by `{internal_id}`')

            return True

        except TicketItemStorageUpdateException as e:
            self.logger.error(f'Could not update the ticket item `{value}` with status `{status}` for account `{internal_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketItemStorage()

        self.log_ticket_item_create_service = LogTicketItemCreateService()
