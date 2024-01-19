from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.security.hasher import Hasher, HasherNonValidException
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.account.model import (
    AccountModel,
    AccountModelPasswordException,
    AccountModelConfirmPasswordException,
    AccountModelConfirmPasswordMismatchException
)

from piracyshield_service.account.set_flag import AccountSetFlagService

from piracyshield_data_storage.account.storage import AccountStorageUpdateException

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

class AccountChangePasswordService(BaseService):

    """
    Changes account password.
    """

    hasher = None

    hasher_config = None

    data_model = None

    data_storage = None

    def __init__(self, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        # child data storage class
        self.data_storage = data_storage()

        self.account_set_flag_service = AccountSetFlagService(data_storage)

        self._prepare_configs()

        self._prepare_modules()

        super().__init__()

    def execute(self, account_id: str, current_password: str, new_password: str, confirm_password: str) -> bool | Exception:
        account_data = self._get_account_data(account_id)

        self._verify_current_password(current_password, account_data.get('password'))

        self._validate_parameters(account_data, new_password, confirm_password)

        if current_password == new_password:
            raise ApplicationException(AccountErrorCode.PASSWORD_DIFF, AccountErrorMessage.PASSWORD_DIFF)

        hashed_new_password = self.hasher.encode_string(new_password)

        try:
            affected_rows = self.data_storage.change_password(
                account_id = account_id,
                password = hashed_new_password
            )

            if not len(affected_rows):
                self.logger.debug(f'Could not change password for account `{account_id}`')

                raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC)

        except AccountStorageUpdateException as e:
            self.logger.error(f'Could not update the account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

        self.account_set_flag_service.execute(
            account_id = account_id,
            flag = 'change_password',
            value = False
        )

        return True

    def _get_account_data(self, account_id: str) -> dict | Exception:
        try:
            response = self.data_storage.get_complete(account_id)

            if response.empty():
                self.logger.debug(f'Could not find any account for `{account_id}`')

                raise ApplicationException(AccountErrorCode.ACCOUNT_NOT_FOUND, AccountErrorMessage.ACCOUNT_NOT_FOUND)

            document = next(response, None)

            return document

        except AccountStorageGetException as e:
            self.logger.error(f'Could not retrieve account `{account_id}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _verify_current_password(self, password: str, hashed_password: str) -> bool | Exception:
        """
        Checks the hashed password against the plain text password.

        :param hashed_password: Argon2 hash string.
        :param password: plain text password to verify.
        """

        try:
            return self.hasher.verify_hash(password, hashed_password)

        except HasherNonValidException:
            raise ApplicationException(AccountErrorCode.PASSWORD_CHANGE_MISMATCH, AccountErrorMessage.PASSWORD_CHANGE_MISMATCH)

    def _schedule_task(self):
        pass

    def _validate_parameters(self, account_data: dict, new_password: str, confirm_password: str) -> bool | Exception:
        try:
            # we currently need to re-validate everything to have a password validation
            self.data_model(
                account_id = account_data.get('account_id'),
                name = account_data.get('name'),
                email = account_data.get('email'),
                password = new_password,
                confirm_password = confirm_password,
                role = account_data.get('role'),
                is_active = account_data.get('is_active')
            )

            return True

        except AccountModelPasswordException:
            raise ApplicationException(AccountErrorCode.PASSWORD_ERROR, AccountErrorMessage.PASSWORD_ERROR)

        except AccountModelConfirmPasswordException:
            raise ApplicationException(AccountErrorCode.PASSWORD_ERROR, AccountErrorMessage.PASSWORD_ERROR)

        except AccountModelConfirmPasswordMismatchException:
            raise ApplicationException(AccountErrorCode.PASSWORD_MISMATCH_ERROR, AccountErrorMessage.PASSWORD_MISMATCH_ERROR)

    def _prepare_configs(self):
        """
        Loads the configs.
        """

        self.hasher_config = Config('security/token').get('hasher')

    def _prepare_modules(self):
        """
        Initialize and set the instances.
        """

        self.data_model = AccountModel

        self.hasher = Hasher(
            time_cost = self.hasher_config.get('time_cost'),
            memory_cost = self.hasher_config.get('memory_cost'),
            parallelism = self.hasher_config.get('parallelism'),
            hash_length = self.hasher_config.get('hash_length'),
            salt_length = self.hasher_config.get('salt_length')
        )
