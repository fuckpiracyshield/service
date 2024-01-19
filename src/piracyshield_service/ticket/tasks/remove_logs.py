from piracyshield_service.task.base import BaseTask

from piracyshield_service.log.ticket.remove_all import LogTicketRemoveAllService

class RemoveLogsTask(BaseTask):

    """
    Operations scheduled on ticket deletion.
    """

    ticket_id = None

    log_ticket_remove_all_service = None

    def __init__(self, ticket_id: str):
        super().__init__()

        self.ticket_id = ticket_id

    def run(self) -> bool:
        """
        Removes the logs for a defined ticket.
        """

        self.log_ticket_remove_all_service.execute(
            ticket_id = self.ticket_id
        )

    def before_run(self):
        """
        Initialize required modules.
        """

        self.log_ticket_remove_all_service = LogTicketRemoveAllService()

    def after_run(self):
        pass

    def on_failure(self):
        pass

def remove_logs_task_caller(**kwargs):
    t = RemoveLogsTask(**kwargs)

    return t.execute()
