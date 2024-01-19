from __future__ import annotations

from piracyshield_service.account.change_password import AccountChangePasswordService

from piracyshield_data_storage.reporter.storage import ReporterStorage

class ReporterChangePasswordService(AccountChangePasswordService):

    """
    Changes password of a reporter account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ReporterStorage)
