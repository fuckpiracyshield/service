from __future__ import annotations

from piracyshield_service.account.exists_by_identifier import AccountExistsByIdentifierService

from piracyshield_data_storage.provider.storage import ProviderStorage

class ProviderExistsByIdentifierService(AccountExistsByIdentifierService):

    """
    Checks if an account with this identifier exists.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ProviderStorage)
