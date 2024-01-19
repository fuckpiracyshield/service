from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageUpdateException

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDASetStatusService(BaseService):

    """
    Sets the status of a DDA identifier.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, dda_id: str, status: bool) -> bool | Exception:
        try:
            affected_rows = self.data_storage.update_status(
                dda_id = dda_id,
                status = status
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not set the status for the DDA identifier')

                raise ApplicationException(DDAErrorCode.CANNOT_SET_STATUS, DDAErrorMessage.CANNOT_SET_STATUS)

        except DDAStorageUpdateException as e:
            self.logger.error(f'Could not update the status of the DDA identifier `{dda_id}`')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

        return True

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = DDAStorage()
