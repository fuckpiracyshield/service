from __future__ import annotations

from piracyshield_service.account.change_password import AccountChangePasswordService

from piracyshield_data_storage.internal.storage import InternalStorage

class InternalChangePasswordService(AccountChangePasswordService):

    """
    Changes password of an internal account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(InternalStorage)
