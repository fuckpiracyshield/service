from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageGetException

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDAExistsByInstanceService(BaseService):

    """
    Check if a DDA instance exists.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, instance: str) -> bool | Exception:
        try:
            response = self.data_storage.exists_by_instance(
                instance = instance
            )

            batch = response.batch()

            if len(batch):
                return True

            return False

        except DDAStorageGetException as e:
            self.logger.error(f'Cannot find DDA instance `{instance}`')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = DDAStorage()
