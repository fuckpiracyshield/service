from __future__ import annotations

from piracyshield_service.account.remove import AccountRemoveService

from piracyshield_data_storage.reporter.storage import ReporterStorage

class ReporterRemoveService(AccountRemoveService):

    """
    Removes a reporter account.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ReporterStorage)
