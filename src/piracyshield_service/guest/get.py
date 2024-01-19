from __future__ import annotations

from piracyshield_service.account.get import AccountGetService

from piracyshield_data_storage.guest.storage import GuestStorage

class GuestGetService(AccountGetService):

    """
    Retrieves a guest account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(GuestStorage)
