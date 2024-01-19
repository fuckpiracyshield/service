from __future__ import annotations

from piracyshield_service.account.set_status import AccountSetStatusService

from piracyshield_data_storage.internal.storage import InternalStorage

class InternalSetStatusService(AccountSetStatusService):

    """
    Sets the status of an internal account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(InternalStorage)
