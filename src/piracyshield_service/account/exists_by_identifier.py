from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageGetException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountExistsByIdentifierService(BaseService):

    """
    Checks if an account with this identifier exists.
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
            response = self.data_storage.exists_by_identifier(
                account_id = account_id
            )

            batch = response.batch()

            if len(batch):
                return True

            return False

        except AccountStorageGetException as e:
            self.logger.error(f'Could not verify if an account exists with the identifier `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
