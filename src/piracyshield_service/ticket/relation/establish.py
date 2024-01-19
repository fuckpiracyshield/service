from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.identifier import Identifier
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.item.genre.model import TicketItemGenreModel

from piracyshield_service.ticket.item.create import TicketItemCreateService
from piracyshield_service.ticket.item.exists_by_value import TicketItemExistsByValueService

from piracyshield_service.ticket.error.get_by_ticket import TicketErrorGetByTicketService

from piracyshield_service.whitelist.exists_by_value import WhitelistExistsByValueService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketRelationEstablishService(BaseService):

    """
    Builds the relation of a ticket items and assigned providers.
    Each ticket item is duplicated and associated to a single provider.
    """

    ticket_item_create_service = None

    whitelist_exists_by_value_service = None

    ticket_error_get_by_ticket_service = None

    ticket_item_exists_by_value_service = None

    identifier = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, providers: list, fqdn: list = None, ipv4: list = None, ipv6: list = None) -> bool | Exception:
        self.logger.debug(f'Establishing relations for `{ticket_id}`')

        fqdn_ticket_items = None
        ipv4_ticket_items = None
        ipv6_ticket_items = None

        if fqdn:
            fqdn_ticket_items = self._establish_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.FQDN.value,
                items = fqdn,
                providers = providers
            )

        if ipv4:
            ipv4_ticket_items = self._establish_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.IPV4.value,
                items = ipv4,
                providers = providers
            )

        if ipv6:
            ipv6_ticket_items = self._establish_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.IPV6.value,
                items = ipv6,
                providers = providers
            )

        self.logger.info(f'Ticket relations completed')

        return (fqdn_ticket_items, ipv4_ticket_items, ipv6_ticket_items)

    def _establish_relation(self, ticket_id: str, genre: str, items: list, providers: list) -> dict:
        ticket_items = []

        for value in items:
            # generate ticket item identifier
            ticket_item_id = self._generate_ticket_item_id()

            is_active = True

            is_duplicate = self._is_duplicate(
                genre = genre,
                value = value
            )

            is_whitelisted = self._is_whitelisted(
                value = value
            )

            is_error = False

            for provider_id in providers:
                self.ticket_item_create_service.execute(
                    ticket_id = ticket_id,
                    ticket_item_id = ticket_item_id,
                    provider_id = provider_id,
                    value = value,
                    genre = genre,
                    is_active = is_active,
                    is_duplicate = is_duplicate,
                    is_whitelisted = is_whitelisted,
                    is_error = is_error
                )

            ticket_items.append({
                'value': value,
                'genre': genre,
                'is_active': is_active,
                'is_duplicate': is_duplicate,
                'is_whitelisted': is_whitelisted,
                'is_error': is_error
            })

        return ticket_items

    def _is_duplicate(self, genre: str, value: str) -> bool:
        found_tickets = self.ticket_item_exists_by_value_service.execute(
            genre = genre,
            value = value
        )

        print(" r -> ", found_tickets)

        # no ticket item found
        if not len(found_tickets):
            return False

        # we have a ticket that contains this ticket item
        if len(found_tickets):
            # but let's search for a ticket error in this case
            for ticket_blocking in found_tickets:
                print(" tb -> ", ticket_blocking)
                ticket_errors = self.ticket_error_get_by_ticket_service.execute(
                    ticket_blocking.get('ticket_id')
                )

                # found one, let's search for our item
                if len(ticket_errors):
                    for ticket_error_response in ticket_errors:
                        print(ticket_error_response)
                        print(ticket_error_response.get(genre))

                        # found the item, so we don't have any duplicate
                        if value in ticket_error_response.get(genre):
                            return False

        return True

    def _is_whitelisted(self, value: str) -> bool:
        return self.whitelist_exists_by_value_service.execute(
            value = value
        )

    def _generate_ticket_item_id(self) -> str:
        """
        Generates a UUIDv4.
        """

        return self.identifier.generate()

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_exists_by_value_service = TicketItemExistsByValueService()

        self.ticket_error_get_by_ticket_service = TicketErrorGetByTicketService()

        self.whitelist_exists_by_value_service = WhitelistExistsByValueService()

        self.ticket_item_create_service = TicketItemCreateService()

        self.identifier = Identifier()
