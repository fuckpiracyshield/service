from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException
from piracyshield_component.security.hasher import Hasher, HasherNonValidException

from piracyshield_data_model.authentication.model import AuthenticationModel, AuthenticationModelEmailException, AuthenticationModelPasswordException

from piracyshield_data_storage.authentication.storage import AuthenticationStorage, AuthenticationStorageGetException

from piracyshield_service.authentication.get import AuthenticationGetService

from piracyshield_service.security.anti_brute_force import SecurityAntiBruteForceService

from piracyshield_service.authentication.errors import AuthenticationErrorCode, AuthenticationErrorMessage

class AuthenticationAuthenticateService(BaseService):

    """
    Credentials based authentication.
    """

    security_anti_brute_force_service = None

    authentication_get_service = None

    data_storage = None

    data_model = None

    hasher = None

    hasher_config = None

    login_config = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, email: str, password: str, ip_address: str) -> dict | Exception:
        # ensure the correctness of the data before proceeding
        model = self._validate_parameters(email, password)

        self.logger.debug(f'Account `{email}` requested an authentication')

        # perform anti brute force controls if active
        if self.security_anti_brute_force_config.get('active') == True:
            self.security_anti_brute_force_service.execute(
                email = email,
                ip_address = ip_address
            )

        account = self.authentication_get_service.execute(
            email = model.get('email')
        )

        # is the account active?
        if account.get('is_active') == False:
            raise ApplicationException(AuthenticationErrorCode.USER_NON_ACTIVE, AuthenticationErrorMessage.USER_NON_ACTIVE)

        # verify password
        self._verify_password(password, account.get('password'))

        self.logger.debug(f"Account `{account.get('email')}` correctly authenticated.")

        return self._build_payload(account)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Checks the hashed password against the plain text password.

        :param hashed_password: Argon2 hash string.
        :param password: plain text password to verify.
        """

        try:
            return self.hasher.verify_hash(password, hashed_password)

        except HasherNonValidException:
            raise ApplicationException(AuthenticationErrorCode.PASSWORD_MISMATCH, AuthenticationErrorMessage.PASSWORD_MISMATCH)

    def _build_payload(self, account: dict) -> dict:
        # TODO: we should pass this via the account service.

        return {
            'account_id': account.get('account_id'),
            'email': account.get('email'),
            'name': account.get('name'),
            'role': account.get('role'),
            'flags': account.get('flags')
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self, email: str, password: str) -> dict | Exception:
        """
        Verify passed parameters using the authentication data model.

        :param email: valid string.
        :param password: valid string.
        """

        try:
            model = self.data_model(email, password)

            return model.to_dict()

        except AuthenticationModelEmailException:
            raise ApplicationException(AuthenticationErrorCode.EMAIL_NON_VALID, AuthenticationErrorMessage.EMAIL_NON_VALID)

        except AuthenticationModelPasswordException:
            raise ApplicationException(AuthenticationErrorCode.PASSWORD_NON_VALID, AuthenticationErrorMessage.PASSWORD_NON_VALID)

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.security_anti_brute_force_config = Config('security/anti_brute_force').get('general')

        self.hasher_config = Config('security/token').get('hasher')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_model = AuthenticationModel

        self.hasher = Hasher(
            time_cost = self.hasher_config.get('time_cost'),
            memory_cost = self.hasher_config.get('memory_cost'),
            parallelism = self.hasher_config.get('parallelism'),
            hash_length = self.hasher_config.get('hash_length'),
            salt_length = self.hasher_config.get('salt_length')
        )

        self.data_storage = AuthenticationStorage()

        self.authentication_get_service = AuthenticationGetService()

        self.security_anti_brute_force_service = SecurityAntiBruteForceService()
