from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageGetException

from piracyshield_service.forensic.errors import ForensicErrorCode, ForensicErrorMessage

class ForensicGetByTicketService(BaseService):

    """
    Returns the forensic data of a ticket by its identifier.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> bool | Exception:
        try:
            response = self.data_storage.get_by_ticket(
                ticket_id = ticket_id
            )

            if response.empty():
                self.logger.debug(f'Could not find any forensic data associated to ticket `{ticket_id}`')

                raise ApplicationException(ForensicErrorCode.NO_HASH_FOR_TICKET, ForensicErrorMessage.NO_HASH_FOR_TICKET)

            document = next(response, None)

            return document

        except ForensicStorageGetException as e:
            self.logger.error(f'Could not get any forensic data for ticket `{ticket_id}`')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = ForensicStorage()
