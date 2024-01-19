from __future__ import annotations

from piracyshield_service.account.get import AccountGetService

from piracyshield_data_storage.internal.storage import InternalStorage

class InternalGetService(AccountGetService):

    """
    Retrieves an internal account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(InternalStorage)
