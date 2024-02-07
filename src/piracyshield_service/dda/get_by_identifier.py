from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageGetException

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDAGetByIdentifierService(BaseService):

    """
    Get a single DDA by its identifier.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, dda_id: str) -> dict | Exception:
        try:
            response = self.data_storage.get_by_identifier(
                dda_id = dda_id
            )

            if response.empty():
                self.logger.debug(f'No DDA found for this identifier `{dda_id}`')

                raise ApplicationException(DDAErrorCode.UNKNOWN_DDA_IDENTIFIER, DDAErrorMessage.UNKNOWN_DDA_IDENTIFIER)

            document = next(response, None)

            return document

        except DDAStorageGetException as e:
            self.logger.error(f'Cannot get the DDA')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = DDAStorage()
