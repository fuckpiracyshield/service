from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.item.processed.model import (
    TicketItemProcessedModel,
    TicketItemProcessedModelProviderIdentifierMissingException,
    TicketItemProcessedModelProviderIdentifierNonValidException,
    TicketItemProcessedModelValueMissingException,
    TicketItemProcessedModelValueNonValidException,
    TicketItemProcessedModelTimestampNonValidException,
    TicketItemProcessedModelNoteNonValidException
)

from piracyshield_data_storage.ticket.item.storage import TicketItemStorage, TicketItemStorageUpdateException

from piracyshield_service.ticket.item.get_by_value import TicketItemGetByValueService

from piracyshield_service.log.ticket.create import LogTicketCreateService
from piracyshield_service.log.ticket.item.create import LogTicketItemCreateService

from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

class TicketItemSetProcessedService(BaseService):

    """
    Sets the ticket item as successfully processed.
    """

    log_ticket_item_create_service = None

    log_ticket_create_service = None

    ticket_item_get_by_value_service = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, provider_id: str, value: str, timestamp: str = None, note: str = None) -> bool | Exception:
        """
        Sets the item status with `PROCESSED`.

        :param provider_id: the associated provider id.
        :param value: the value of the ticket item.
        :param timestamp: optional valid ISO8601 date.
        :param note: optional string.
        :return
        """

        model = self._validate_parameters(
            provider_id = provider_id,
            value = value,
            timestamp = timestamp,
            note = note
        )

        ticket_item_data = self.ticket_item_get_by_value_service.execute(
            provider_id = provider_id,
            value = value
        )

        # check if ticket item update time is expired
        if Time.is_expired(
            ticket_item_data.get('metadata').get('created_at'),
            expiration_time = ticket_item_data.get('settings').get('update_max_time')
        ) == True:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_UPDATE_TIME_EXCEEDED, TicketItemErrorMessage.TICKET_ITEM_UPDATE_TIME_EXCEEDED)

        try:
            affected_rows = self.data_storage.update_status_by_value(
                provider_id = model.get('provider_id'),
                value = model.get('value'),
                status = model.get('status'),
                updated_at = Time.now_iso8601(),
                timestamp = model.get('timestamp'),
                note = model.get('note')
            )

            if not len(affected_rows):
                self.logger.debug(f'No ticket item found for `{value}` requested by {provider_id}')

                raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOT_FOUND, TicketItemErrorMessage.TICKET_ITEM_NOT_FOUND)

            ticket_item = list(affected_rows).__getitem__(0)

            # log on parent ticket level
            self.log_ticket_create_service.execute(
                ticket_id = ticket_item.get('ticket_id'),
                message = f'Updated {value} status to `{model.get("status")}` by `{provider_id}`.'
            )

            # log on a ticket item level
            self.log_ticket_item_create_service.execute(
                ticket_item_id = ticket_item.get('ticket_item_id'),
                message = f'Updated with status to `{model.get("status")}` by `{provider_id}`.'
            )

            self.logger.debug(f'Status `{model.get("status")}` set for {value} by {provider_id}')

            return True

        except TicketItemStorageUpdateException as e:
            self.logger.error(f'Could not update the ticket item `{value}` for account `{provider_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _validate_parameters(self, provider_id: str, value: str, timestamp: str = None, note: str = None):
        try:
            model = self.data_model(
                provider_id = provider_id,
                value = value,
                timestamp = timestamp,
                note = note
            )

            return model.to_dict()

        except TicketItemProcessedModelProviderIdentifierMissingException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_PROVIDER_ID_MISSING, TicketItemErrorMessage.TICKET_ITEM_PROVIDER_ID_MISSING)

        except TicketItemProcessedModelProviderIdentifierNonValidException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_PROVIDER_ID_NON_VALID, TicketItemErrorMessage.TICKET_ITEM_PROVIDER_ID_NON_VALID)

        except TicketItemProcessedModelValueMissingException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_VALUE_MISSING, TicketItemErrorMessage.TICKET_ITEM_VALUE_MISSING)

        except TicketItemProcessedModelValueNonValidException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_VALUE_NON_VALID, TicketItemErrorMessage.TICKET_ITEM_VALUE_NON_VALID)

        except TicketItemProcessedModelTimestampNonValidException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_TIMESTAMP_NON_VALID, TicketItemErrorMessage.TICKET_ITEM_TIMESTAMP_NON_VALID)

        except TicketItemProcessedModelNoteNonValidException:
            raise ApplicationException(TicketItemErrorCode.TICKET_ITEM_NOTE_NON_VALID, TicketItemErrorMessage.TICKET_ITEM_NOTE_NON_VALID)

    def _schedule_task(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketItemProcessedModel

        self.data_storage = TicketItemStorage()

        self.ticket_item_get_by_value_service = TicketItemGetByValueService()

        self.log_ticket_create_service = LogTicketCreateService()

        self.log_ticket_item_create_service = LogTicketItemCreateService()
