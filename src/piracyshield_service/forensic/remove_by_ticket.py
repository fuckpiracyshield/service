from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageRemoveException

from piracyshield_service.forensic.errors import ForensicErrorCode, ForensicErrorMessage

class ForensicRemoveByTicketService(BaseService):

    """
    Removes the forensic data for a ticket.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> bool | Exception:
        """
        :param ticket_id: a ticket identifier.
        :return: true if everything is successful.
        """

        try:
            self.data_storage.remove_by_ticket(
                ticket_id = ticket_id
            )

            self.logger.debug(f'Removed forensic hashes for ticket `{ticket_id}`')

        except ForensicStorageRemoveException as e:
            self.logger.error(f'Could not remove the forensic evidence for ticket `{ticket_id}`')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

        return True

    def _validate_parameters(self):
        pass

    def _schedule_task(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        """
        Initialize and set the instances.
        """

        self.data_storage = ForensicStorage()
