from __future__ import annotations

from piracyshield_service.account.get import AccountGetService

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderGetService(AccountGetService):

    """
    Retrieves a provider account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ProviderStorage)
