from __future__ import annotations

from piracyshield_service.account.get_all import AccountGetAllService

from piracyshield_data_storage.guest.storage import GuestStorage

class GuestGetAllService(AccountGetAllService):

    """
    Retrieves all the guest accounts.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(GuestStorage)
