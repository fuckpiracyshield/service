from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_data_storage.account.general.storage import GeneralAccountStorage, GeneralAccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class GeneralAccountGetAllService(BaseService):

    """
    Fetches all the accounts.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self) -> list:
        try:
            response = self.data_storage.get_all()

            if response.empty():
                self.logger.debug(f'No account found')

                raise ApplicationException(AccountErrorCode.ACCOUNT_NOT_FOUND, AccountErrorMessage.ACCOUNT_NOT_FOUND)

            batch = response.batch()

            return list(batch)

        except GeneralAccountStorageGetException:
            self.logger.error(f'Could not get the account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = GeneralAccountStorage()
