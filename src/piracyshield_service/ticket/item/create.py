from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.item.model import TicketItemModel

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageCreateException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemCreateService(BaseService):

    """
    Creates a new ticket item.
    """

    data_model = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self,
        ticket_id: str,
        ticket_item_id: str,
        provider_id: str,
        value: str,
        genre: str,
        is_active: bool,
        is_duplicate: bool,
        is_whitelisted: bool,
        is_error: bool
    ) -> bool | Exception:
        """
        :param ticket_id: ticket identifier associated to the ticket item.
        :param ticket_item_id: random generated identifier.
        :param provider_id: account identifier that will handle this ticket item.
        :param value: a valid FQDN or IPv4.
        :param genre: FQDN or IPv4 type.
        :return
        """

        model = self._validate_parameters(
            ticket_id = ticket_id,
            ticket_item_id = ticket_item_id,
            value = value,
            genre = genre,
            provider_id = provider_id,
            is_active = is_active,
            is_duplicate = is_duplicate,
            is_whitelisted = is_whitelisted,
            is_error = is_error
        )

        document = self._build_document(
            model = model,
            now = Time.now_iso8601()
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except TicketItemStorageCreateException as e:
            self.logger.error(f'Could not create the ticket item `{document.get("value")}` for `{document.get("ticket_id")}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

        self.logger.info(f'Ticket item `{document.get("value")}` created for ticket `{document.get("ticket_id")}`')

        return True

    def _build_document(self, model: dict, now: str) -> dict:
        return {
            'ticket_id': model.get('ticket_id'),
            'ticket_item_id': model.get('ticket_item_id'),
            'provider_id': model.get('provider_id'),
            'value': model.get('value'),
            'genre': model.get('genre'),
            'status': model.get('status'),
            'is_active': model.get('is_active'),
            'is_duplicate': model.get('is_duplicate'),
            'is_whitelisted': model.get('is_whitelisted'),
            'is_error': model.get('is_error'),
            'settings': model.get('settings'),
            'metadata': {
                'created_at': now,
                'updated_at': now
            }
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self,
        ticket_id: str,
        ticket_item_id: str,
        provider_id: str,
        value: str,
        genre: str,
        is_active: bool,
        is_duplicate: bool,
        is_whitelisted: bool,
        is_error: bool
    ):
        try:
            model = self.data_model(
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

            return model.to_dict()

        # this has been already validated by the ticket service, but better safe than sorry
        except Exception as e:
            self.logger.error(f'Could not create the ticket item `{value}` for `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketItemModel

        self.data_storage = TicketItemStorage()
