from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountGetTotalService(BaseService):

    """
    Retrieves the total number of accounts.
    """

    data_storage = None

    def __init__(self, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        # child data storage class
        self.data_storage = data_storage()

        super().__init__()

    def execute(self) -> list | Exception:
        try:
            response = self.data_storage.get_total()

            batch = response.batch()

            return len(batch)

        except AccountStorageGetException as e:
            self.logger.error(f'Could not retrieve the total count of the accounts')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = AccountStorage()
