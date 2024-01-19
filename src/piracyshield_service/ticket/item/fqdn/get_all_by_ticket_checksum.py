from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.checksum import Checksum
from piracyshield_component.exception import ApplicationException

from piracyshield_service.ticket.item.fqdn.get_all_by_ticket import TicketItemFQDNGetAllByTicketService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemFQDNGetAllByTicketChecksumService(BaseService):

    """
    Returns the checksum of the FQDN list of a ticket.
    """

    checksum = None

    ticket_item_fqdn_get_all_by_ticket_service = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> list | Exception:
        """
        Get the checksum of all the FQDN items by ticket_id.

        :return
        """

        response = self.ticket_item_fqdn_get_all_by_ticket_service.execute(
            ticket_id = ticket_id
        )

        data = '\n'.join(response)

        try:
            return self.checksum.from_string(
                algorithm = 'sha256',
                string = data
            )

        except ChecksumUnicodeException as e:
            self.logger.error(f'Could not generate the checksum for FQDN for ticket `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_fqdn_get_all_by_ticket_service = TicketItemFQDNGetAllByTicketService()

        self.checksum = Checksum()
