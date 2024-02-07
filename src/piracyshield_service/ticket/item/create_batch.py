from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.item.model import TicketItemModel

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageCreateException

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemCreateBatchService(BaseService):

    """
    Create multiple ticket items in a single batch.
    """

    data_model = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_items: list) -> bool | Exception:
        """
        :param ticket_items: a list of ticket items dictionaries.
        :return
        """

        batch = []

        for ticket_item in ticket_items:
            model = self._validate_parameters(**ticket_item)

            batch.append(self._build_document(
                model = model,
                now = Time.now_iso8601()
            ))

        try:
            # insert the data into the database
            self.data_storage.insert_many(batch)

        except TicketItemStorageCreateException as e:
            self.logger.error(f'Could not massively create ticket items')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

        self.logger.info(f'Created {len(batch)} ticket items')

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
            self.logger.error(f'Could not validate ticket item `{value}` for `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketItemModel

        self.data_storage = TicketItemStorage()
