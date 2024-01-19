from __future__ import annotations

from piracyshield_service.account.remove import AccountRemoveService

from piracyshield_data_storage.guest.storage import GuestStorage

class GuestRemoveService(AccountRemoveService):

    """
    Removes a guest account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(GuestStorage)
