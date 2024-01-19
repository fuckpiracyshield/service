from __future__ import annotations

from piracyshield_service.account.remove import AccountRemoveService

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderRemoveService(AccountRemoveService):

    """
    Removes a provider account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ProviderStorage)
