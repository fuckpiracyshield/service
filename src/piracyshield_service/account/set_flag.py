from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.account.storage import AccountStorageUpdateException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountSetFlagService(BaseService):

    """
    Sets the flag of an account.
    """

    data_storage = None

    def __init__(self, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        # child data storage class
        self.data_storage = data_storage()

        super().__init__()

    def execute(self, account_id: str, flag: str, value: any) -> bool | Exception:
        try:
            affected_rows = self.data_storage.set_flag(
                account_id = account_id,
                flag = flag,
                value = value
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not update the flag for account `{account_id}`')

                raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC)

            return True

        except AccountStorageUpdateException as e:
            self.logger.error(f'Could not update the flag for account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
