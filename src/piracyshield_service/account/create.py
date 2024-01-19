from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.utils.time import Time
from piracyshield_component.security.hasher import Hasher, HasherGenericException
from piracyshield_component.security.identifier import Identifier
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.account.model import (
    AccountModel,
    AccountModelNameException,
    AccountModelEmailException,
    AccountModelPasswordException,
    AccountModelConfirmPasswordException,
    AccountModelConfirmPasswordMismatchException,
    AccountModelRoleException
)

from piracyshield_data_model.account.flags.model import (
    AccountFlagsModel,
    AccountFlagsModelUnknownFlagException,
    AccountFlagsModelValueException
)

from piracyshield_data_storage.authentication.storage import AuthenticationStorage, AuthenticationStorageGetException
from piracyshield_data_storage.account.storage import AccountStorage, AccountStorageCreateException

from piracyshield_service.authentication.exists_by_email import AuthenticationExistsByEmailService

from piracyshield_service.account.errors import AccountErrorCode, AccountErrorMessage

from collections import deque

class AccountCreateService(BaseService):

    """
    Account creation class.
    """

    authentication_exists_by_email_service = None

    authentication_storage = None

    flags_data_model = None

    data_model = None

    data_storage = None

    hasher = None

    hasher_config = None

    identifier = None

    def __init__(self, data_model: AccountModel, data_storage: AccountStorage):
        """
        Inizialize logger and required modules.
        """

        self.data_model = data_model

        self.data_storage = data_storage()

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, name: str, email: str, password: str, confirm_password: str, flags: dict, created_by: str) -> str | Exception:
        """
        :param name: a string that identificates the real name (and, eventually, sourname) of the user.
        :param email: e-mail address, used in conjunction with a password to authenticate the user.
        :param password: a string.
        :param confirm_password: must be the same as `password`.
        :param flags: flags of the account.
        :param created_by: account id of the creator.
        :return account id of the created user.
        """

        model = self._validate_parameters(
            account_id = self._generate_account_id(),
            name = name,
            email = email,
            password = password,
            confirm_password = confirm_password,
            is_active = True
        )

        # check for duplicates
        if self.authentication_exists_by_email_service.execute(
            email = model.get('email')
        ) == True:
            raise ApplicationException(AccountErrorCode.EMAIL_EXISTS, AccountErrorMessage.EMAIL_EXISTS)

        flags_model = self._validate_flags(
            flags = flags
        )

        document = self._build_document(
            model = model,
            encoded_password = self.hasher.encode_string(model.get('password')),
            created_by = created_by,
            flags = flags_model,
            now = Time.now_iso8601()
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except AccountStorageCreateException as e:
            self.logger.error(f'Could not create the account')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

        self.logger.info(f'Account `{document.get("email")}` created with id `{document.get("account_id")}`')

        # return the pre-generated user_id
        return document.get('account_id')

    def _generate_account_id(self) -> str:
        """
        Generates a UUIDv4 to use as a main account identifier without exposing the true ID in the database.
        """

        return self.identifier.generate()

    def _encode_password(self, password: str) -> str | Exception:
        """
        Attempts to encode the plain test password.

        :param password: plain text password.
        :return: a string containing the encoded password.
        """

        try:
            return self.hasher.encode_string(password)

        except HasherGenericException as e:
            self.logger.error(f'Could not encode password `{password}`')

            raise ApplicationException(AccountErrorCode.GENERIC, AccountErrorMessage.GENERIC, e)

    def _build_document(self, model: dict, encoded_password: str, created_by: str, flags: dict, now: str) -> dict:
        return {
            'account_id': model.get('account_id'),
            'name': model.get('name'),
            'email': model.get('email'),
            'password': encoded_password,
            'role': model.get('role'),
            'is_active': model.get('is_active'),
            'flags': flags.get('flags'),
            'metadata': {
                # creation date
                'created_at': now,

                # same as creation date
                'updated_at': now,

                # who created this item
                'created_by': created_by
            }
        }

    def _schedule_task(self):
        pass

    def _validate_flags(self, flags: dict) -> dict:
        try:
            # validate flags
            model = self.flags_data_model(
                flags = flags
            )

            return model.to_dict()

        except AccountFlagsModelUnknownFlagException:
            raise ApplicationException(AccountErrorCode.FLAG_UNKNOWN, AccountErrorMessage.FLAG_UNKNOWN)

        except AccountFlagsModelValueException:
            raise ApplicationException(AccountErrorCode.FLAG_NON_VALID_VALUE, AccountErrorMessage.FLAG_NON_VALID_VALUE)

    def _validate_parameters(self, account_id: str, name: str, email: str, password: str, confirm_password: str, is_active: bool) -> dict:
        try:
            # validate given parameters
            model = self.data_model(
                account_id = account_id,
                name = name,
                email = email,
                password = password,
                confirm_password = confirm_password,
                is_active = True
            )

            return model.to_dict()

        except AccountModelNameException:
            raise ApplicationException(AccountErrorCode.NAME_ERROR, AccountErrorMessage.NAME_ERROR)

        except AccountModelEmailException:
            raise ApplicationException(AccountErrorCode.EMAIL_ERROR, AccountErrorMessage.EMAIL_ERROR)

        except AccountModelPasswordException:
            raise ApplicationException(AccountErrorCode.PASSWORD_ERROR, AccountErrorMessage.PASSWORD_ERROR)

        except AccountModelConfirmPasswordException:
            raise ApplicationException(AccountErrorCode.PASSWORD_ERROR, AccountErrorMessage.PASSWORD_ERROR)

        except AccountModelConfirmPasswordMismatchException:
            raise ApplicationException(AccountErrorCode.PASSWORD_MISMATCH_ERROR, AccountErrorMessage.PASSWORD_MISMATCH_ERROR)

        # this is implicitly passed by the child model
        except AccountModelRoleException:
            raise ApplicationException(AccountErrorCode.ROLE_ERROR, AccountErrorMessage.ROLE_ERROR)

    def _prepare_configs(self):
        """
        Loads the configs.
        """

        self.hasher_config = Config('security/token').get('hasher')

    def _prepare_modules(self):
        """
        Initialize and set the instances.
        """

        self.flags_data_model = AccountFlagsModel

        self.hasher = Hasher(
            time_cost = self.hasher_config.get('time_cost'),
            memory_cost = self.hasher_config.get('memory_cost'),
            parallelism = self.hasher_config.get('parallelism'),
            hash_length = self.hasher_config.get('hash_length'),
            salt_length = self.hasher_config.get('salt_length')
        )

        self.identifier = Identifier()

        self.authentication_storage = AuthenticationStorage()

        self.authentication_exists_by_email_service = AuthenticationExistsByEmailService()
