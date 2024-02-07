from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.identifier import Identifier
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.item.genre.model import TicketItemGenreModel
from piracyshield_data_model.whitelist.genre.model import WhitelistGenreModel

from piracyshield_service.ticket.item.create_batch import TicketItemCreateBatchService
from piracyshield_service.ticket.item.get_active import TicketItemGetActiveService

from piracyshield_service.whitelist.get_active import WhitelistGetActiveService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

from piracyshield_component_cidr_verifier import is_ipv4_in_cidr, is_ipv6_in_cidr

class TicketRelationEstablishService(BaseService):

    """
    Builds the relation of a ticket items and assigned providers.
    Each ticket item is created and associated to a single provider.
    """

    batch = []

    ticket_item_cache = {}

    whitelist_cache = {}

    ticket_item_create_service = None

    ticket_item_get_active_service = None

    whitelist_get_active_service = None

    identifier = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

        # build ticket item cache
        self._build_ticket_item_cache()

        # build whitelist cache
        self._build_whitelist_cache()

    def execute(self, ticket_id: str, providers: list, fqdn: list = None, ipv4: list = None, ipv6: list = None) -> bool | Exception:
        self.batch = []

        self.logger.debug(f'Establishing relations for `{ticket_id}`')

        fqdn_ticket_items = None
        ipv4_ticket_items = None
        ipv6_ticket_items = None

        if fqdn:
            fqdn_ticket_items = self._generate_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.FQDN.value,
                items = fqdn,
                providers = providers
            )

        if ipv4:
            ipv4_ticket_items = self._generate_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.IPV4.value,
                items = ipv4,
                providers = providers
            )

        if ipv6:
            ipv6_ticket_items = self._generate_relation(
                ticket_id = ticket_id,
                genre = TicketItemGenreModel.IPV6.value,
                items = ipv6,
                providers = providers
            )

        # insert batch
        self.ticket_item_create_batch_service.execute(self.batch)

        self.logger.info(f'Ticket relations completed')

        return (fqdn_ticket_items, ipv4_ticket_items, ipv6_ticket_items)

    def _generate_relation(self, ticket_id: str, genre: str, items: list, providers: list) -> dict:
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
                genre = genre,
                value = value
            )

            is_error = False

            for provider_id in providers:
                self.batch.append({
                    'ticket_id': ticket_id,
                    'ticket_item_id': ticket_item_id,
                    'value': value,
                    'genre': genre,
                    'provider_id': provider_id,
                    'is_active': is_active,
                    'is_duplicate': is_duplicate,
                    'is_whitelisted': is_whitelisted,
                    'is_error': is_error
                })

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
        if genre == TicketItemGenreModel.FQDN.value and TicketItemGenreModel.FQDN.value in self.ticket_item_cache:
            return value in self.ticket_item_cache.get(TicketItemGenreModel.FQDN.value)

        elif genre == TicketItemGenreModel.IPV4.value and TicketItemGenreModel.IPV4.value in self.ticket_item_cache:
            return value in self.ticket_item_cache.get(TicketItemGenreModel.IPV4.value)

        elif genre == TicketItemGenreModel.IPV6.value and TicketItemGenreModel.IPV6.value in self.ticket_item_cache:
            return value in self.ticket_item_cache.get(TicketItemGenreModel.IPV6.value)

        return False

    def _is_whitelisted(self, genre: str, value: str) -> bool:
        if genre == TicketItemGenreModel.FQDN.value and TicketItemGenreModel.FQDN.value in self.whitelist_cache:
            return value in self.whitelist_cache.get(WhitelistGenreModel.FQDN.value)

        elif genre == TicketItemGenreModel.IPV4.value and TicketItemGenreModel.IPV4.value in self.whitelist_cache:
            if value in self.whitelist_cache.get(WhitelistGenreModel.IPV4.value):
                return True

            if WhitelistGenreModel.CIDR_IPV4.value in self.whitelist_cache:
                for cidr_ipv4 in self.whitelist_cache.get(WhitelistGenreModel.CIDR_IPV4.value):
                    if is_ipv4_in_cidr(value, cidr_ipv4) == True:
                        return True

        elif genre == TicketItemGenreModel.IPV6.value and TicketItemGenreModel.IPV6.value in self.whitelist_cache:
            if value in self.whitelist_cache.get(WhitelistGenreModel.IPV6.value):
                return True

            if WhitelistGenreModel.CIDR_IPV6.value in self.whitelist_cache:
                for cidr_ipv6 in self.whitelist_cache.get(WhitelistGenreModel.CIDR_IPV6.value):
                    if is_ipv6_in_cidr(value, cidr_ipv6) == True:
                        return True

        return False

    def _generate_ticket_item_id(self) -> str:
        """
        Generates a UUIDv4.
        """

        return self.identifier.generate()

    def _build_ticket_item_cache(self):
        self.ticket_item_cache = self.ticket_item_get_active_service.execute()

    def _build_whitelist_cache(self):
        self.whitelist_cache = self.whitelist_get_active_service.execute()

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_get_active_service = TicketItemGetActiveService()

        self.ticket_item_create_batch_service = TicketItemCreateBatchService()

        self.whitelist_get_active_service = WhitelistGetActiveService()

        self.identifier = Identifier()
