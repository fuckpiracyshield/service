from piracyshield_service.task.base import BaseTask

from piracyshield_data_model.forensic.archive.status.model import ForensicArchiveStatusModel

from piracyshield_forensic.analyze import ForensicAnalysis

from piracyshield_service.forensic.update_archive_status import ForensicUpdateArchiveStatusService

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_component.exception import ApplicationException

class AnalyzeForensicArchiveTask(BaseTask):

    """
    Forensic evidence archive integrity analysis procedure.
    """

    data_storage_cache = None

    log_ticket_create_service = None

    update_archive_status_service = None

    ticket_id = None

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

        self.update_archive_status_service.execute(
            ticket_id = self.ticket_id,
            status = ForensicArchiveStatusModel.APPROVED.value
        )

        # log success operation
        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_id,
            message = f'The forensic evidence has been successfully approved.'
        )

        return True

    def before_run(self):
        """
        Initialize required modules.
        """

        self.log_ticket_create_service = LogTicketCreateService()

        self.forensic_analysis = ForensicAnalysis()

        self.update_archive_status_service = ForensicUpdateArchiveStatusService()

    def after_run(self):
        pass

    def on_failure(self):
        pass

def analyze_forensic_archive_task_caller(**kwargs):
    t = AnalyzeForensicArchiveTask(**kwargs)

    return t.execute()
