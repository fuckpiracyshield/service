from piracyshield_service.task.base import BaseTask

from piracyshield_data_model.ticket.status.model import TicketStatusModel

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageUpdateException

from piracyshield_service.log.ticket.create import LogTicketCreateService

class TicketInitializeTask(BaseTask):

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
        Starts the operations for the new ticket.
        The status gets set to `open` as we make it visible for API pulls and notifications
        """

        # TODO: must check if the ticket exists.

        # change status
        try:
            self.ticket_storage.update_status(
                ticket_id = self.ticket_id,
                ticket_status = TicketStatusModel.OPEN.value
            )

        except TicketStorageUpdateException:
            self.logger.error(f'Could not update the ticket `{self.ticket_id}`')

        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_id,
            message = f'Changed status to `{TicketStatusModel.OPEN.value}`.'
        )

    def before_run(self):
        """
        Initialize required modules.
        """
        self.ticket_storage = TicketStorage()

        self.log_ticket_create_service = LogTicketCreateService()

    def after_run(self):
        pass

    def on_failure(self):
        pass

def ticket_initialize_task_caller(**kwargs):
    t = TicketInitializeTask(**kwargs)

    return t.execute()
