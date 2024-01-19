from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountGetAllService(BaseService):

    """
    Fetches all accounts.
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
            response = self.data_storage.get_all()

            batch = response.batch()

            if not len(batch):
                self.logger.debug(f'No account found')

                raise ApplicationException(AccountErrorCode.ACCOUNT_NOT_FOUND, AccountErrorMessage.ACCOUNT_NOT_FOUND)

            return list(batch)

        except AccountStorageGetException as e:
            self.logger.error(f'Could not retrieve any account')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
