from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.checksum import Checksum
from piracyshield_component.exception import ApplicationException

from piracyshield_service.ticket.item.ipv6.get_all_by_provider import TicketItemIPv6GetAllByProviderService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemIPv6GetAllChecksumByProviderService(BaseService):

    """
    Returns the checksum of all the tickets' IPv6 lists assigned to a provider.
    """

    checksum = None

    ticket_item_ipv6_get_all_by_provider_service = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, account_id: str) -> str:
        """
        Get the checksum of all the IPv6 items in the database.

        :return
        """

        response = self.ticket_item_ipv6_get_all_by_provider_service.execute(
            account_id = account_id
        )

        data = '\n'.join(response)

        try:
            return self.checksum.from_string(
                algorithm = 'sha256',
                string = data
            )

        except ChecksumUnicodeException as e:
            self.logger.error(f'Could not generate the checksum for IPv6s')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_ipv6_get_all_by_provider_service = TicketItemIPv6GetAllByProviderService()

        self.checksum = Checksum()
