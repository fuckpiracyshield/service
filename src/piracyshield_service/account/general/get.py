from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_data_storage.account.general.storage import GeneralAccountStorage, GeneralAccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class GeneralAccountGetService(BaseService):

    """
    Fetches any type of account.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, account_id: str) -> dict:
        try:
            response = self.data_storage.get(account_id)

            if response.empty():
                self.logger.debug(f'Could not find any account for `{account_id}`')

                raise ApplicationException(AccountErrorCode.ACCOUNT_NOT_FOUND, AccountErrorMessage.ACCOUNT_NOT_FOUND)

            document = next(response, None)

            return document

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
