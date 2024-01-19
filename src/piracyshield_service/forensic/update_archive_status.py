from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageUpdateException

from piracyshield_service.forensic.errors import ForensicErrorCode, ForensicErrorMessage

class ForensicUpdateArchiveStatusService(BaseService):

    """
    Updates the status of a previously uploaded archive.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, status: str, reason: str = None) -> bool | Exception:
        """
        :param ticket_id: a ticket identifier.
        :param status: status of the analysis.
        :param reason: optional reason for non successful statuses.
        :return: true if everything is successful.
        """

        try:
            self.data_storage.update_archive_status(
                ticket_id = ticket_id,
                status = status,
                updated_at = Time.now_iso8601(),
                reason = reason
            )

            self.logger.debug(f'Updated forensic evidence status for ticket `{ticket_id}` with status `{status}`')

        except ForensicStorageUpdateException as e:
            self.logger.error(f'Could not update the status of the forensic evidence for ticket `{ticket_id}` with status `{status}`')

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
