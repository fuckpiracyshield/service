from __future__ import annotations

from piracyshield_service.account.get_all import AccountGetAllService

from piracyshield_data_storage.internal.storage import InternalStorage

class InternalGetAllService(AccountGetAllService):

    """
    Retrieves all the internal accounts.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(InternalStorage)
