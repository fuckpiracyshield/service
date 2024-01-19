from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_service.ticket.item.remove_all import TicketItemRemoveAllService

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketRelationAbandonService(BaseService):

    """
    Removes the relationship.
    """

    ticket_item_remove_all_service = None

    identifier = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str) -> str | Exception:
        self.logger.debug(f'Removing relations for `{ticket_id}`')

        self.ticket_item_remove_all_service.execute(ticket_id)

        self.logger.info(f'Removed all the items for `{ticket_id}`')

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.ticket_item_remove_all_service = TicketItemRemoveAllService()
