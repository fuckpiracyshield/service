from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageRemoveException

from piracyshield_service.ticket.has_dda_id import TicketHasDDAIdService

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDARemoveService(BaseService):

    """
    Removes a DDA identifier.
    """

    ticket_has_dda_id_service = None

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, dda_id: str) -> None | Exception:
        try:
            # check if no tickets uses this DDA instance
            if self.ticket_has_dda_id_service.execute(
                dda_id = dda_id
            ):
                raise ApplicationException(DDAErrorCode.INSTANCE_USED, DDAErrorMessage.INSTANCE_USED)

            affected_rows = self.data_storage.remove(
                dda_id = dda_id
            )

            if not affected_rows:
                raise ApplicationException(DDAErrorCode.CANNOT_REMOVE, DDAErrorMessage.CANNOT_REMOVE)

        except DDAStorageRemoveException as e:
            self.logger.error(f'Cannot remove DDA `{value}`')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = DDAStorage()

        self.ticket_has_dda_id_service = TicketHasDDAIdService()
