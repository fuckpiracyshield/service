from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountGetService(BaseService):

    """
    Fetches account data.
    """

    data_storage = None

    def __init__(self, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        # child data storage class
        self.data_storage = data_storage()

        super().__init__()

    def execute(self, account_id: str) -> dict | Exception:
        try:
            response = self.data_storage.get(account_id)

            if response.empty():
                self.logger.debug(f'Could not find any account for `{account_id}`')

                raise ApplicationException(AccountErrorCode.ACCOUNT_NOT_FOUND, AccountErrorMessage.ACCOUNT_NOT_FOUND)

            document = next(response, None)

            return document

        except AccountStorageGetException as e:
            self.logger.error(f'Could not retrieve account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
