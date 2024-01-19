from __future__ import annotations

from piracyshield_service.account.remove import AccountRemoveService

from piracyshield_data_storage.internal.storage import InternalStorage

class InternalRemoveService(AccountRemoveService):

    """
    Removes an internal account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(InternalStorage)
