from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageGetException

from piracyshield_service.whitelist.errors import WhitelistErrorCode, WhitelistErrorMessage

class WhitelistGetActiveService(BaseService):

    """
    Get all the active whitelist items.

    This is currently used to build a cache.
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
            response = self.data_storage.get_active()

            document = next(response, None)

            return document

        except WhitelistStorageGetException as e:
            self.logger.error(f'Cannot get all the whitelist items')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = WhitelistStorage()
