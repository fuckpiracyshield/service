from __future__ import annotations

from piracyshield_service.account.create import AccountCreateService

from piracyshield_data_model.provider.model import ProviderModel

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderCreateService(AccountCreateService):

    """
    Creates a provider account.
    """

    def __init__(self):
        """
        Pass the data model and data storage to the parent class.
        """

        super().__init__(ProviderModel, ProviderStorage)

    def execute(self, name: str, email: str, password: str, confirm_password: str, flags: dict, created_by: str) -> str | Exception:
        """
        :param name: a string that identificates the real name (and, eventually, sourname) of the account.
        :param email: e-mail address, used in conjunction with a password to authenticate the account.
        :param password: a string.
        :param confirm_password: must be the same as `password`.
        :param flags: flags of the account.
        :param created_by: account id of the creator.
        :return account id of the created account.
        """

        return super().execute(name, email, password, confirm_password, flags, created_by)
