from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException

from piracyshield_service.authentication.verify_refresh_token import AuthenticationVerifyRefreshTokenService
from piracyshield_service.authentication.generate_access_token import AuthenticationGenerateAccessTokenService

from piracyshield_service.account.session.find_long_session import AccountSessionFindLongSessionService
from piracyshield_service.account.session.create_short_session import AccountSessionCreateShortSessionService

from piracyshield_service.security.anti_brute_force import SecurityAntiBruteForceService

from piracyshield_service.authentication.errors import AuthenticationErrorCode, AuthenticationErrorMessage

class AuthenticationRefreshAccessTokenService(BaseService):

    """
    Refreshes the access token provided a valid and active refresh token.
    """

    authentication_generate_access_token_service = None

    authentication_verify_refresh_token_service = None

    account_session_find_long_session_service = None

    account_session_create_short_session_service = None

    jwt_token_config = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, refresh_token: str, ip_address: str) -> dict | Exception:
        # TODO: verify if blacklisted.

        # verify the token and unwrap the payload
        payload = self.authentication_verify_refresh_token_service.execute(
            token = refresh_token
        )

        # retrieve the long session data so we can check out which account identifier is assigned to this new token
        long_session = self.account_session_find_long_session_service.execute(
            refresh_token = refresh_token
        )

        account_id = None

        if long_session:
            (_, account_id, _, _) = long_session.split(':')

        else:
            self.logger.error(f"Could not find a long session for this refresh token `{refresh_token}`")

            raise ApplicationException(AuthenticationErrorCode.GENERIC, AuthenticationErrorMessage.GENERIC)

        access_token = self.authentication_generate_access_token_service.execute(payload)

        # create a new session for this user
        self.account_session_create_short_session_service.execute(
            refresh_token = refresh_token,
            access_token = access_token,
            account_id = account_id,
            ip_address = ip_address
        )

        return access_token

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.jwt_token_config = Config('security/token').get('jwt_token')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.authentication_verify_refresh_token_service = AuthenticationVerifyRefreshTokenService()

        self.authentication_generate_access_token_service = AuthenticationGenerateAccessTokenService()

        self.account_session_find_long_session_service = AccountSessionFindLongSessionService()

        self.account_session_create_short_session_service = AccountSessionCreateShortSessionService()
