from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageRemoveException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountRemoveService(BaseService):

    """
    Removes an account.
    """

    data_storage = None

    def __init__(self, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        # child data storage class
        self.data_storage = data_storage()

        super().__init__()

    def execute(self, account_id: str) -> bool | Exception:
        try:
            self.data_storage.remove(account_id)

            return True

        except AccountStorageRemoveException as e:
            self.logger.error(f'Could not remove the account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
