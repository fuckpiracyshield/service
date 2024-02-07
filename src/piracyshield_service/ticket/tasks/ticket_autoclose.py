from piracyshield_service.task.base import BaseTask

from piracyshield_data_model.ticket.status.model import TicketStatusModel

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageUpdateException

from piracyshield_service.log.ticket.create import LogTicketCreateService

class TicketAutocloseTask(BaseTask):

    """
    Operations scheduled after the creation of a ticket.
    """

    ticket_id = None

    ticket_storage = None

    log_ticket_create_service = None

    def __init__(self, ticket_id: str):
        super().__init__()

        self.ticket_id = ticket_id

    def run(self) -> bool:
        """
        Auto-closes the ticket after 30 minutes.
        This ticket will not be visible anymore to the providers.
        """

        # TODO: must check if the ticket exists.

        # change status
        self.ticket_storage.update_status(
            ticket_id = self.ticket_id,
            ticket_status = TicketStatusModel.CLOSED.value
        )

    def before_run(self):
        """
        Initialize required modules.
        """
        self.ticket_storage = TicketStorage()

        self.log_ticket_create_service = LogTicketCreateService()

    def after_run(self):
        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_id,
            message = f'Changed status to `{TicketStatusModel.CLOSED.value}`.'
        )

    def on_failure(self):
        self.logger.error(f'Could not update the ticket `{self.ticket_id}`')

        self.ticket_storage.update_status(
            ticket_id = self.ticket_id,
            ticket_status = TicketStatusModel.CREATED.value
        )

def ticket_autoclose_task_caller(**kwargs):
    t = TicketAutocloseTask(**kwargs)

    return t.execute()
