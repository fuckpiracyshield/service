from piracyshield_service.task.base import BaseTask

from piracyshield_component.utils.time import Time

from piracyshield_data_model.ticket.status.model import TicketStatusModel

from piracyshield_data_storage.ticket.storage import TicketStorage

from piracyshield_service.ticket.relation.establish import TicketRelationEstablishService
from piracyshield_service.ticket.relation.abandon import TicketRelationAbandonService
from piracyshield_service.ticket.get import TicketGetService

from piracyshield_service.forensic.remove_by_ticket import ForensicRemoveByTicketService

from piracyshield_service.ticket.tasks.ticket_initialize import ticket_initialize_task_caller
from piracyshield_service.ticket.tasks.ticket_autoclose import ticket_autoclose_task_caller

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_service.task.service import TaskService

class TicketCreateTask(BaseTask):

    """
    Creation of ticket items and subsequent tasks.
    """

    pending_tasks = []

    ticket_data = None

    ticket_relation_establish_service = None

    ticket_relation_abandon_service = None

    ticket_get_service = None

    ticket_storage = None

    log_ticket_create_service = None

    task_service = None

    def __init__(self, ticket_data: dict):
        super().__init__()

        self.ticket_data = ticket_data

    def run(self) -> bool:
        """
        Starts the operations for the new ticket.
        The status gets set to `open` as we make it visible for API pulls and notifications
        """

        # proceed to build the relation item <-> provider
        # this part provides a check for duplicates, whitelisted items and error tickets
        (fqdn_ticket_items, ipv4_ticket_items, ipv6_ticket_items) = self.ticket_relation_establish_service.execute(
            ticket_id = self.ticket_data.get('ticket_id'),
            providers = self.ticket_data.get('assigned_to'),
            fqdn = self.ticket_data.get('fqdn') or None,
            ipv4 = self.ticket_data.get('ipv4') or None,
            ipv6 = self.ticket_data.get('ipv6') or None
        )

        self.pending_tasks.append(self.task_service.create(
            task_caller = ticket_initialize_task_caller,
            delay = self.ticket_data.get('settings').get('revoke_time'),
            ticket_id = self.ticket_data.get('ticket_id')
        ))

        self.pending_tasks.append(self.task_service.create(
            task_caller = ticket_autoclose_task_caller,
            delay = self.ticket_data.get('settings').get('autoclose_time'),
            ticket_id = self.ticket_data.get('ticket_id')
        ))

        self.ticket_storage.update_task_list(
            ticket_id = self.ticket_data.get('ticket_id'),
            task_ids = self.pending_tasks,
            updated_at = Time.now_iso8601()
        )

        return True

    def before_run(self):
        """
        Initialize required modules.
        """

        self.ticket_storage = TicketStorage()

        self.ticket_get_service = TicketGetService()

        self.ticket_relation_establish_service = TicketRelationEstablishService()

        self.ticket_relation_abandon_service = TicketRelationAbandonService()

        self.forensic_remove_by_ticket_service = ForensicRemoveByTicketService()

        self.log_ticket_create_service = LogTicketCreateService()

        self.task_service = TaskService()

    def after_run(self):
        self.ticket_storage.update_status(
            ticket_id = self.ticket_data.get('ticket_id'),
            ticket_status = TicketStatusModel.CREATED.value
        )

        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = self.ticket_data.get('ticket_id'),
            message = f'Completed the creation of all ticket items.'
        )

    def on_failure(self):
        self.logger.error(f'Could not initialize ticket items for `{self.ticket_data.get("ticket_id")}`')

        self.ticket_relation_abandon_service.execute(self.ticket_data.get('ticket_id'))

        self.forensic_remove_by_ticket_service.execute(self.ticket_data.get('ticket_id'))

        for single_task in self.pending_tasks:
            self.task_service.remove(single_task)

        self.ticket_storage.update_status(
            ticket_id = self.ticket_data.get('ticket_id'),
            ticket_status = TicketStatusModel.FAILED.value
        )

def ticket_create_task_caller(**kwargs):
    t = TicketCreateTask(**kwargs)

    return t.execute()
