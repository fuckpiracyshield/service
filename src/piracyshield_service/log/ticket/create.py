from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.log.ticket.storage import LogTicketStorage, LogTicketStorageCreateException

from piracyshield_data_model.log.ticket.model import (
    LogTicketModel,
    LogTicketModelTicketIdentifierMissingException,
    LogTicketModelTicketIdentifierNonValidException,
    LogTicketModelMessageNonValidException,
    LogTicketModelMessageMissingException
)

from piracyshield_service.log.ticket.errors import LogTicketErrorCode, LogTicketErrorMessage

class LogTicketCreateService(BaseService):

    """
    Creates a new ticket log record.
    """

    data_storage = None

    data_model = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, message: str) -> bool | Exception:
        model = self._validate_parameters(
            ticket_id = ticket_id,
            message = message
        )

        document = self._build_document(
            model = model,
            now = Time.now_iso8601()
        )

        try:
            self.data_storage.insert(document)

            return True

        except LogTicketStorageCreateException as e:
            self.logger.error(f'Could not create the log entry')

            raise ApplicationException(LogTicketErrorCode.GENERIC, LogTicketErrorMessage.GENERIC, e)

    def _build_document(self, model: dict, now: str) -> dict:
        return {
            'ticket_id': model.get('ticket_id'),
            'message': model.get('message'),
            'metadata': {
                # creation date
                'created_at': now
            }
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self, ticket_id: str, message: str):
        try:
            model = self.data_model(
                ticket_id = ticket_id,
                message = message
            )

            return model.to_dict()

        except LogTicketModelTicketIdentifierMissingException:
            raise ApplicationException(LogTicketErrorCode.MISSING_TICKET_ID, LogTicketErrorMessage.MISSING_TICKET_ID)

        except LogTicketModelTicketIdentifierNonValidException:
            raise ApplicationException(LogTicketErrorCode.NON_VALID_TICKET_ID, LogTicketErrorMessage.NON_VALID_TICKET_ID)

        except LogTicketModelMessageMissingException:
            raise ApplicationException(LogTicketErrorCode.MISSING_MESSAGE, LogTicketErrorMessage.MISSING_MESSAGE)

        except LogTicketModelMessageNonValidException:
            raise ApplicationException(LogTicketErrorCode.NON_VALID_MESSAGE, LogTicketErrorMessage.NON_VALID_MESSAGE)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = LogTicketModel

        self.data_storage = LogTicketStorage()
