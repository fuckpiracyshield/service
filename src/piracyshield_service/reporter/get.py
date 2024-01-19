from __future__ import annotations

from piracyshield_service.account.get import AccountGetService

from piracyshield_data_storage.reporter.storage import ReporterStorage

class ReporterGetService(AccountGetService):

    """
    Retrieves a reporter account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ReporterStorage)
