from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.checksum import Checksum
from piracyshield_component.exception import ApplicationException

from piracyshield_service.ticket.item.ipv4.get_all_by_ticket import TicketItemIPv4GetAllByTicketService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv4GetAllByTicketChecksumService(BaseService):

    """
    Returns the checksum of the IPv4 list of a ticket.
    """

    checksum = None

    ticket_item_ipv4_get_all_by_ticket_service = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> list | Exception:
        """
        Get the checksum of all the IPv4 items by ticket_id.

        :return
        """

        response = self.ticket_item_ipv4_get_all_by_ticket_service.execute(
            ticket_id = ticket_id
        )

        data = '\n'.join(response)

        try:
            return self.checksum.from_string(
                algorithm = 'sha256',
                string = data
            )

        except ChecksumUnicodeException as e:
            self.logger.error(f'Could not generate the checksum for IPv4 for ticket `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_ipv4_get_all_by_ticket_service = TicketItemIPv4GetAllByTicketService()

        self.checksum = Checksum()
