from __future__ import annotations

from piracyshield_service.account.set_status import AccountSetStatusService

from piracyshield_data_storage.reporter.storage import ReporterStorage

class ReporterSetStatusService(AccountSetStatusService):

    """
    Sets the status of a reporter account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ReporterStorage)
