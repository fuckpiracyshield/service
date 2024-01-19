from __future__ import annotations

from piracyshield_service.account.change_password import AccountChangePasswordService

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderChangePasswordService(AccountChangePasswordService):

    """
    Changes password of a provider account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ProviderStorage)
