from __future__ import annotations

from piracyshield_service.account.get_all import AccountGetAllService

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderGetActiveService(AccountGetAllService):

    """
    Retrieves all the active provider accounts.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ProviderStorage)
