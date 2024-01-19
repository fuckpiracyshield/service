from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.log.ticket.item.storage import LogTicketItemStorage, LogTicketItemStorageCreateException

from piracyshield_data_model.log.ticket.item.model import (
    LogTicketItemModel,
    LogTicketItemModelTicketItemIdentifierMissingException,
    LogTicketItemModelTicketItemIdentifierNonValidException,
    LogTicketItemModelMessageNonValidException,
    LogTicketItemModelMessageMissingException
)

from piracyshield_service.log.ticket.item.errors import LogTicketItemErrorCode, LogTicketItemErrorMessage

class LogTicketItemCreateService(BaseService):

    """
    Creates a new ticket item log record.
    """

    data_storage = None

    data_model = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_item_id: str, message: str) -> bool | Exception:
        model = self._validate_parameters(
            ticket_item_id = ticket_item_id,
            message = message
        )

        document = self._build_document(
            model = model,
            now = Time.now_iso8601()
        )

        try:
            self.data_storage.insert(document)

            return True

        except LogTicketItemStorageCreateException as e:
            self.logger.error(f'Could not create the ticket item log record')

            raise ApplicationException(LogTicketItemErrorCode.GENERIC, LogTicketItemErrorMessage.GENERIC, e)

    def _build_document(self, model: dict, now: str) -> dict:
        return {
            'ticket_item_id': model.get('ticket_item_id'),
            'message': model.get('message'),
            'metadata': {
                # creation date
                'created_at': now
            }
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self, ticket_item_id: str, message: str):
        try:
            model = self.data_model(
                ticket_item_id = ticket_item_id,
                message = message
            )

            return model.to_dict()

        except LogTicketItemModelTicketItemIdentifierMissingException:
            raise ApplicationException(LogTicketItemErrorCode.MISSING_TICKET_ITEM_ID, LogTicketItemErrorMessage.MISSING_TICKET_ITEM_ID)

        except LogTicketItemModelTicketItemIdentifierNonValidException:
            raise ApplicationException(LogTicketItemErrorCode.NON_VALID_TICKET_ITEM_ID, LogTicketItemErrorMessage.NON_VALID_TICKET_ITEM_ID)

        except LogTicketItemModelMessageMissingException:
            raise ApplicationException(LogTicketItemErrorCode.MISSING_MESSAGE, LogTicketItemErrorMessage.MISSING_MESSAGE)

        except LogTicketItemModelMessageNonValidException:
            raise ApplicationException(LogTicketItemErrorCode.NON_VALID_MESSAGE, LogTicketItemErrorMessage.NON_VALID_MESSAGE)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = LogTicketItemModel

        self.data_storage = LogTicketItemStorage()
