from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageGetException

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDAGetGlobalService(BaseService):

    """
    Get all the DDA identifiers.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self) -> list | Exception:
        try:
            response = self.data_storage.get_global()

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No DDA identifier found')

            return list(batch)

        except DDAStorageGetException as e:
            self.logger.error(f'Cannot get all the DDA identifiers')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = DDAStorage()
