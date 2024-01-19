from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.exception import ApplicationException
from piracyshield_component.security.token import JWTToken, JWTTokenExpiredException, JWTTokenNonValidException

from piracyshield_service.authentication.errors import AuthenticationErrorCode, AuthenticationErrorMessage

class AuthenticationVerifyRefreshTokenService(BaseService):

    """
    Verifies a refresh token.
    """

    token = None

    jwt_config = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, token: bytes) -> dict | Exception:
        """
        Verifies the validity of the JWT token and unrolls the payload.

        :param token: a valid JWT token string.
        """

        try:
            return self.token.verify_refresh_token(token)

        except JWTTokenExpiredException:
            raise ApplicationException(AuthenticationErrorCode.TOKEN_EXPIRED, AuthenticationErrorMessage.TOKEN_EXPIRED)

        except JWTTokenNonValidException:
            raise ApplicationException(AuthenticationErrorCode.TOKEN_MISMATCH, AuthenticationErrorMessage.TOKEN_MISMATCH)

    def _schedule_task(self):
        pass

    def _validate_parameters(self, email: str, password: str) -> dict | Exception:
        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.jwt_config = Config('security/token').get('jwt_token')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.token = JWTToken(
            access_secret_key = self.jwt_config.get('access_secret_key'),
            refresh_secret_key = self.jwt_config.get('refresh_secret_key'),
            access_expiration_time = self.jwt_config.get('access_expiration_time'),
            refresh_expiration_time = self.jwt_config.get('refresh_expiration_time'),
            algorithm = self.jwt_config.get('algorithm')
        )
