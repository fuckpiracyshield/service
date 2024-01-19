from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.authentication.storage import AuthenticationStorage, AuthenticationStorageGetException

from piracyshield_service.authentication.errors import AuthenticationErrorCode, AuthenticationErrorMessage

class AuthenticationGetService(BaseService):

    """
    Retrieves an account.
    """

    data_storage = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, email: str) -> dict | Exception:
        try:
            response = self.data_storage.get(
                email = email
            )

            if response.empty():
                self.logger.debug(f'Could not find any account for `{email}`')

                raise ApplicationException(AuthenticationErrorCode.EMAIL_NOT_FOUND, AuthenticationErrorMessage.EMAIL_NOT_FOUND)

            document = next(response, None)

            return document

        except AuthenticationStorageGetException as e:
            self.logger.error(f'Could not verify if e-mail exists')

            raise ApplicationException(AuthenticationErrorCode.GENERIC, AuthenticationErrorMessage.GENERIC, e)

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_storage = AuthenticationStorage()
