from piracyshield_service.task.base import BaseTask

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.forensic.archive.status.model import ForensicArchiveStatusModel

from piracyshield_forensic.analyze import ForensicAnalysis

from piracyshield_service.forensic.update_archive_status import ForensicUpdateArchiveStatusService
from piracyshield_service.forensic.get_by_ticket import ForensicGetByTicketService

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageUpdateException

class AnalyzeForensicArchiveTask(BaseTask):

    """
    Forensic evidence archive integrity analysis procedure.
    """

    data_storage_cache = None

    log_ticket_create_service = None

    update_archive_status_service = None

    get_by_ticket_service = None

    ticket_id = None

    data_storage = None

    def __init__(self, ticket_id: str):
        super().__init__()

        self.ticket_id = ticket_id

    def run(self) -> bool:
        """
        Performs the analysis and updates the ticket.
        """

        self.update_archive_status_service.execute(
            ticket_id = self.ticket_id,
            status = ForensicArchiveStatusModel.IN_PROGRESS.value
        )

        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_id,
            message = f'Started a new forensic archive analysis.'
        )

        try:
            # perform analysis.
            self.forensic_analysis.process(self.ticket_id)

        except ApplicationException as e:
            self.logger.error(f'Could not process the forensic evidence for ticket `{self.ticket_id}`: {e.message}')

            self.update_archive_status_service.execute(
                ticket_id = self.ticket_id,
                status = ForensicArchiveStatusModel.REJECTED.value,
                reason = e.message
            )

            self.log_ticket_create_service.execute(
                ticket_id = self.ticket_id,
                message = f'The forensic evidence has been rejected: {e.message}'
            )

            return False

        # NOTE: we won't clean the package from the cache here as we might want to schedule a cleaning process separately.

        # retrieve forensic data associated to this ticket identifier
        forensic_data = self.get_by_ticket_service.execute(
            ticket_id = self.ticket_id
        )

        # get other tickets with the same hash, if any
        tickets = self._hash_string_exists(
            hash_string = forensic_data.get('hash_string')
        )

        for ticket_data in tickets:
            self.data_storage.update_archive_name(
                ticket_id = ticket_data.get('ticket_id'),
                archive_name = forensic_data.get('archive_name'),
                status = ForensicArchiveStatusModel.APPROVED.value,
                updated_at = Time.now_iso8601()
            )

        # log success operation
        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_id,
            message = f'The forensic evidence has been successfully approved.'
        )

        return True

    def _hash_string_exists(self, hash_string: str) -> bool | Exception:
        try:
            response = self.data_storage.exists_hash_string(
                hash_string = hash_string
            )

            if response.empty():
                return False

            return list(response.batch())

        except ForensicStorageGetException as e:
            self.logger.error(f'Could not verify `{hash_string}` existence')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

    def before_run(self):
        """
        Initialize required modules.
        """

        self.data_storage = ForensicStorage()

        self.log_ticket_create_service = LogTicketCreateService()

        self.forensic_analysis = ForensicAnalysis()

        self.get_by_ticket_service = ForensicGetByTicketService()

        self.update_archive_status_service = ForensicUpdateArchiveStatusService()

    def after_run(self):
        pass

    def on_failure(self):
        pass

def analyze_forensic_archive_task_caller(**kwargs):
    t = AnalyzeForensicArchiveTask(**kwargs)

    return t.execute()
