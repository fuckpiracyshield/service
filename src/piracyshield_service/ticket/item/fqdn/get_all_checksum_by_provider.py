from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.checksum import Checksum
from piracyshield_component.exception import ApplicationException

from piracyshield_service.ticket.item.fqdn.get_all_by_provider import TicketItemFQDNGetAllByProviderService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemFQDNGetAllChecksumByProviderService(BaseService):

    """
    Returns the checksum of all the tickets' FQDN lists assigned to a provider.
    """

    checksum = None

    ticket_item_fqdn_get_all_by_provider_service = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, account_id: str) -> str | Exception:
        """
        Get the checksum of all the FQDN items in the database.

        :return
        """

        response = self.ticket_item_fqdn_get_all_by_provider_service.execute(
            account_id = account_id
        )

        data = '\n'.join(response)

        try:
            return self.checksum.from_string(
                algorithm = 'sha256',
                string = data
            )

        except ChecksumUnicodeException as e:
            self.logger.error(f'Could not generate the checksum for FQDNs')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_fqdn_get_all_by_provider_service = TicketItemFQDNGetAllByProviderService()

        self.checksum = Checksum()
