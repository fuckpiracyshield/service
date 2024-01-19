from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageGetException, TicketStorageRemoveException

from piracyshield_service.ticket.relation.abandon import TicketRelationAbandonService

from piracyshield_service.ticket.get import TicketGetService

from piracyshield_service.ticket.tasks.remove_logs import remove_logs_task_caller

from piracyshield_service.forensic.remove_by_ticket import ForensicRemoveByTicketService

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

from datetime import datetime, timedelta

class TicketRemoveService(BaseService):

    """
    Removes a ticket within the allowed time.
    """

    ticket_get_service = None

    ticket_relation_abandon_service = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> bool | Exception:
        # document = self._get_ticket(ticket_id)
        document = self.ticket_get_service.execute(
            ticket_id = ticket_id
        )

        # check if ticket is expired
        if Time.is_expired(
            date = document.get('metadata').get('created_at'),
            expiration_time = document.get('settings').get('revoke_time')
        ) == True:
            raise ApplicationException(TicketErrorCode.REVOKE_TIME_EXCEEDED, TicketErrorMessage.REVOKE_TIME_EXCEEDED)

        # TODO: have a centralized tasks collection and service to do this.

        # if not, proceed to cancel each associated task
        for task in document.get('tasks'):
            self.task_service.remove(task)

        # this removal operation is only available within the revoke time process (75s as per today),
        # therefore we don't need to have any other deletion process than the main ticket
        self._schedule_task(
            ticket_id = document.get('ticket_id')
        )

        # remove ticket items
        self.ticket_relation_abandon_service.execute(
            ticket_id = document.get('ticket_id')
        )

        # remove associated forensic evidence
        self.forensic_remove_by_ticket_service.execute(
            ticket_id = document.get('ticket_id')
        )

        # finally remove the ticket
        try:
            self.data_storage.remove(
                ticket_id = document.get('ticket_id')
            )

            return True

        except TicketStorageRemoveException as e:
            self.logger.error(f'Could not remove ticket `{ticket_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _schedule_task(self, ticket_id: str):
        try:
            self.task_service.create(
                task_caller = remove_logs_task_caller,
                delay = 1,
                ticket_id = ticket_id
            )

        except Exception as e:
            self.logger.error(f'Could not remove tasks for ticket `{ticket_id}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = TicketStorage()

        self.forensic_remove_by_ticket_service = ForensicRemoveByTicketService()

        self.ticket_relation_abandon_service = TicketRelationAbandonService()

        self.ticket_get_service = TicketGetService()
